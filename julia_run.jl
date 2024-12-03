using JuMP
using Gurobi
using CSV
using DataFrames
using HDF5
using Base.Threads

S = parse(Int, ARGS[1])
alpha = parse(Float64, ARGS[2])
N = parse(Int, ARGS[3])

Tx = CSV.read("real_distances/drop_distance_matrix.csv", DataFrame, drop=1:1)[1:N, 1:N] |> Matrix #N, N
Ty = CSV.read("real_distances/distance_matrix_store_to_drop.csv",DataFrame, drop=1:1)[:, 1:N] |> Matrix; #M, N
Tz = CSV.read("real_distances/drop_to_store_distance_matrix.csv",DataFrame, drop=1:1)[1:N, :] |> Matrix; #N, M

M,N = size(Ty)

Cf = 1
Cw = 1
Ct = 3
println("a: ", alpha)
println("M: ", M)
println("N: ", N)
println("S: ", S)

model = Model(Gurobi.Optimizer)
set_optimizer_attribute(model, "TimeLimit", 60 * 60 * 7)

@variable(model, o[1:M], Bin)
@variable(model, x[1:S, 1:N, 1:N], Bin)
@variable(model, y[1:S, 1:M, 1:N], Bin)
@variable(model, z[1:S, 1:N, 1:M], Bin)
@variable(model, f[1:S] >= 0)
@variable(model, u[1:N] >= 1)
@variable(model, L >= 0)


# @objective(model, Min, (Cf*sum(o[i] for i in 1:M) + 
# Ct * sum(y[k, i, j] for k in 1:S, i in 1:M, j in 1:N) + 
# Cw * sum(sum(y[k,i,j]*Ty[i,j] + z[k,j,i]*Tz[j,i] for i in 1:M, j in 1:N) + sum(x[k, j1, j2] * Tx[j1, j2] for j1 in 1:N, j2 in 1:N) for k in 1:S)))


@objective(model, Min, alpha*(Cf*sum(o[i] for i in 1:M) + 
Ct * sum(y[k, i, j] for k in 1:S, i in 1:M, j in 1:N) + 
Cw * sum(sum(y[k,i,j]*Ty[i,j] + z[k,j,i]*Tz[j,i] for i in 1:M, j in 1:N) + sum(x[k, j1, j2] * Tx[j1, j2] for j1 in 1:N, j2 in 1:N) for k in 1:S)) +
(1 - alpha) * L)

#MTZ Constraitns
@constraint(model, [j=1:N], u[j] <= N)
  

#(MTZ) Between Demand Locations
@constraint(model, [j1=1:N, j2=1:N; j1 != j2], u[j2] - u[j1] >= 1 - N * (1 - sum(x[k, j1, j2] for k in 1:S)))


# Optional additional constriant

@constraint(model, [j=1:N, k=1:S],x[k,j,j] == 0)

# end additional constraint

#A truck can leave from at most one factory

@constraint(model, [k=1:S], sum(y[k,i,j] for i in 1:M, j in 1:N) <= 1)


#Trucks can only travel if they first leave from a factory 

@constraint(model, [k=1:S], sum(x[k,j1,j2] for j1 in 1:N, j2 in 1:N) <= (N - 1) * sum(y[k,i,j] for i in 1:M, j in 1:N))


#Trucks can only leave used factories

@constraint(model, [i=1:M], sum(y[k,i,j] for k in 1:S, j in 1:N) <= S * o[i]) #changed this from N to S


#Trucks start and end at the same factory

@constraint(model, [k=1:S, i=1:M], sum(z[k,j,i] for j in 1:N) == sum(y[k,i,j] for j in 1:N))


#FLOW CONSTRAINTS
#SUM IN = 1
@constraint(model, [j2=1:N], sum(sum(y[k,i,j2] for i in 1:M) + sum(x[k,j1,j2] for j1 in 1:N) for k in 1:S) == 1)


# for j1 in 1:N  #SUM OUT = 1
#     @constraint(model, sum(sum(x[k,j1,j2] for j2 in 1:N) + sum(z[k,j1,i] for i in 1:M) for k in 1:S) == 1)
# end 

#If truck k enters location j, it must exit location j

@constraint(model, [j=1:N, k=1:S],(sum(y[k,i,j] for i in 1:M) + sum(x[k,j1,j] for j1 in 1:N)) == (sum(x[k,j,j2] for j2 in 1:N) + sum(z[k,j,i] for i in 1:M)) )


# Time constraints

@constraint(model, [k=1:S], f[k] == sum(y[k,i,j] * Ty[i,j] for i in 1:M, j in 1:N) + sum(x[k,j1,j2] * Tx[j1,j2] for j1 in 1:N, j2 in 1:N))



@constraint(model, [k=1:S], f[k] <= L)

optimize!(model)


try
    rm("results/output.h5")
catch
    1
end
h5write("results/output.h5", "factories", value.(o))
h5write("results/output.h5", "x_edges", value.(x))
h5write("results/output.h5", "y_edges", value.(y))
h5write("results/output.h5", "z_edges", value.(z))
