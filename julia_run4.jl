using JuMP
using Gurobi
using CSV
using DataFrames
using HDF5
using Base.Threads


alpha = parse(Float64, ARGS[1])

N = 4356
directory = ARGS[2]

Tx = CSV.read(directory * "/demand_distance.csv", DataFrame, drop=1:1) |> Matrix #N, N
Ty = CSV.read(directory * "/store_demand_distance.csv", DataFrame, drop=1:1) |> Matrix; #M, N
Tz = CSV.read(directory * "/demand_store_distance.csv", DataFrame, drop=1:1) |> Matrix; #N, M

M,N = size(Ty)

Cf = 3
Cw = .01
Ct = 1
println("a: ", alpha)
println("M: ", M)
println("N: ", N)

model = Model(Gurobi.Optimizer)
#set_optimizer_attribute(model, "TimeLimit", 60 * 60 * 7) #for real
set_optimizer_attribute(model, "TimeLimit", 60 * 60) #for simulated


# @variable(model, o[1:M], Bin)
@variable(model, x[1:M, 1:N, 1:N], Bin)
@variable(model, y[1:M, 1:N], Bin)
@variable(model, z[1:N, 1:M], Bin)
@variable(model, f[1:M] >= 0)
@variable(model, u[1:N] >= 1)
@variable(model, L >= 0)


# @objective(model, Min, (Cf*sum(o[i] for i in 1:M) + 
# Ct * sum(y[k, i, j] for k in 1:S, i in 1:M, j in 1:N) + 
# Cw * sum(sum(y[k,i,j]*Ty[i,j] + z[k,j,i]*Tz[j,i] for i in 1:M, j in 1:N) + sum(x[k, j1, j2] * Tx[j1, j2] for j1 in 1:N, j2 in 1:N) for k in 1:S)))


@objective(model, Min, alpha*(Cf*M + 
Ct * M + 
Cw * sum(sum(y[i,j]*Ty[i,j] + z[j,i]*Tz[j,i] for i in 1:M, j in 1:N) + sum(x[k, j1, j2] * Tx[j1, j2] for j1 in 1:N, j2 in 1:N) for k in 1:M)) +
(1 - alpha) * L)

#MTZ Constraitns
@constraint(model, [j=1:N], u[j] <= N)
  
#(MTZ) Between Demand Locations
@constraint(model, [j1=1:N, j2=1:N; j1 != j2], u[j2] - u[j1] >= 1 - N * (1 - sum(x[k, j1, j2] for k in 1:M)))


# Optional additional constriant
@constraint(model, [j=1:N, k=1:M],x[k,j,j] == 0)

# end additional constraint

#A truck can leave from at most one factory

# @constraint(model, [k=1:S], sum(y[k, i,j] for i in 1:M, j in 1:N) <= 1)


# Factory path must start at a factory
@constraint(model, [k=1:M], sum(x[k,j1,j2] for j1 in 1:N, j2 in 1:N) <= (N - 1) * sum(y[k,j] for j in 1:N))


#Trucks can only leave used factories  -----NOW ALL FACTORIES USED
# @constraint(model, [i=1:M], sum(y[k,i,j] for k in 1:S, j in 1:N) <= S * o[i]) #changed this from N to S


#Trucks start and end at the same factory Now just start and stop same number of times meaningless
@constraint(model, [i=1:M], sum(z[j,i] for j in 1:N) == sum(y[i,j] for j in 1:N))


#FLOW CONSTRAINTS
#SUM IN = 1
@constraint(model, [j2=1:N], sum(y[k,j2] + sum(x[k,j1,j2] for j1 in 1:N) for k in 1:M) == 1)


# for j1 in 1:N  #SUM OUT = 1
#     @constraint(model, sum(sum(x[k,j1,j2] for j2 in 1:N) + sum(z[k,j1,i] for i in 1:M) for k in 1:S) == 1)
# end 

#If Factory k enters location j, it must exit location j

@constraint(model, [j=1:N, k=1:M],(y[k,j] + sum(x[k,j1,j] for j1 in 1:N)) == (sum(x[k,j,j2] for j2 in 1:N) + z[j,k]) )


# Time constraints

@constraint(model, [k=1:M], f[k] == sum(y[k,j] * Ty[k,j] for j in 1:N) + sum(x[k,j1,j2] * Tx[j1,j2] for j1 in 1:N, j2 in 1:N))

# I think missing a condtition for whether a factory exists by just seeing if an edge goes out of it

@constraint(model, [k=1:M], f[k] <= L)

optimize!(model)


try
    rm(directory * "/baseline_output.h5")
catch
    1
end
h5write(directory * "/baseline_output.h5", "factories", value.(o))
h5write(directory * "/baseline_output.h5", "x_edges", value.(x))
h5write(directory * "/baseline_output.h5", "y_edges", value.(y))
h5write(directory * "/base_lineoutput.h5", "z_edges", value.(z))
