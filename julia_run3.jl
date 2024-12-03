using JuMP
using Gurobi
using CSV
using DataFrames
using HDF5
using Base.Threads

S = parse(Int, ARGS[1])
alpha = parse(Float64, ARGS[2])

N = 4356
directory = ARGS[3]

Tx = CSV.read(directory * "/demand_distance.csv", DataFrame, drop=1:1) |> Matrix #N, N
Ty = CSV.read(directory * "/store_demand_distance.csv", DataFrame, drop=1:1) |> Matrix; #M, N
Tz = CSV.read(directory * "/demand_store_distance.csv", DataFrame, drop=1:1) |> Matrix; #N, M

function filter_distance_matrix(matrix, threshold)
    M, N = size(matrix)
    filtered_edges = Dict()  # Initialize an empty dictionary

    for i in 1:M
        for j in 1:N
            if matrix[i, j] <= threshold
                # Store the distance value with the key as the (i, j) tuple
                filtered_edges[(i, j)] = matrix[i, j]
            end
        end
    end

    return filtered_edges
end

# Example usage
distance_threshold = 10000.0  # Example threshold
filtered_Tx = filter_distance_matrix(Tx, distance_threshold)
filtered_Ty = filter_distance_matrix(Ty, distance_threshold)
filtered_Tz = filter_distance_matrix(Tz, distance_threshold)
# println(filtered_Tz)
M,N = size(Ty)

Cf = 1
Cw = 0
Ct = 100
println("a: ", alpha)
println("M: ", M)
println("N: ", N)
println("S: ", S)

model = Model(Gurobi.Optimizer)
set_optimizer_attribute(model, "TimeLimit", 60 * 60 * 7)

println("Demand->Demand Edges: ", length(filtered_Tx))
println("Factory->Demand Edges: ", length(filtered_Ty))
println("Demand->Factory Edges: ", length(filtered_Tz))



@variable(model, o[1:M], Bin)
@variable(model, x[k=1:S, (j1, j2) in keys(filtered_Tx)], Bin)
@variable(model, y[k=1:S, (i, j) in keys(filtered_Ty)], Bin)
@variable(model, z[k=1:S, (j, i) in keys(filtered_Tz)], Bin)
@variable(model, f[1:S] >= 0)
@variable(model, u[1:N] >= 1)
@variable(model, L >= 0)

println("Variables Created")

# @objective(model, Min, (Cf*sum(o[i] for i in 1:M) + 
# Ct * sum(y[k, i, j] for k in 1:S, i in 1:M, j in 1:N) + 
# Cw * sum(sum(y[k,i,j]*Ty[i,j] + z[k,j,i]*Tz[j,i] for i in 1:M, j in 1:N) + sum(x[k, j1, j2] * Tx[j1, j2] for j1 in 1:N, j2 in 1:N) for k in 1:S)))


# @objective(model, Min, alpha*(Cf*sum(o[i] for i in 1:M) + 
# Ct * sum(y[k, i, j] for k in 1:S, i in 1:M, j in 1:N) + 
# Cw * sum(sum(y[k,i,j]*Ty[i,j] + z[k,j,i]*Tz[j,i] for i in 1:M, j in 1:N) + sum(x[k, j1, j2] * Tx[j1, j2] for j1 in 1:N, j2 in 1:N) for k in 1:S)) +
# (1 - alpha) * L)

# @objective(model, Min, alpha * (Cf * sum(o[i] for i in 1:M) + 
# Ct * sum(y[k, i, j] for k in 1:S, (i, j) in filtered_Ty) + 
# Cw * sum(sum(y[k, i, j] * Ty[i, j] for (i, j) in filtered_Ty) + 
#          sum(z[k, j, i] * Tz[j, i] for (j, i) in filtered_Tz) + 
#          sum(x[k, j1, j2] * Tx[j1, j2] for (j1, j2) in filtered_Tx)) for k in 1:S) + 
# (1 - alpha) * L)

@objective(model, Min,
    alpha * (
        Cf * sum(o[i] for i in 1:M) + Ct * sum(y[k, (i, j)] for k in 1:S, (i, j) in keys(filtered_Ty)) + 
        Cw * (
             sum(y[k, (i, j)] * Ty[i, j] for k in 1:S, (i, j) in keys(filtered_Ty)) +
             sum(z[k, (j, i)] * Tz[j, i] for k in 1:S, (j, i) in keys(filtered_Tz)) + 
             sum(x[k, (j1, j2)] * Tx[j1, j2] for k in 1:S, (j1, j2) in keys(filtered_Tx))
        )
    ) +
    (1 - alpha) * L
)

# @objective(model, Min, L)
println("Objective Formulated")

#MTZ Constraitns
@constraint(model, [j=1:N], u[j] <= N)
  

#(MTZ) Between Demand Locations
# @constraint(model, [j1=1:N, j2=1:N; j1 != j2], u[j2] - u[j1] >= 1 - N * (1 - sum(x[k, j1, j2] for k in 1:S)))
# @constraint(model, [(j1, j2) in filtered_Tx; j1 != j2],
#     u[j2] - u[j1] >= 1 - N * (1 - sum(x[k, j1, j2] for k in 1:S))
# )
@constraint(model, [(j1, j2) in keys(filtered_Tx); j1 != j2],
    u[j2] - u[j1] >= 1 - N * (1 - sum(x[k, (j1, j2)] for k in 1:S))
)

println("Finished MTZ")
# Optional additional constriant

# @constraint(model, [j=1:N, k=1:S],x[k,j,j] == 0)
@constraint(model, [j=1:N, k=1:S], x[k, (j, j)] == 0)

println("Finished No Self Loops")

# end additional constraint

#A truck can leave from at most one factory

# @constraint(model, [k=1:S], sum(y[k, (i, j)] for i in 1:M, j in 1:N) <= 1)
@constraint(model, [k=1:S], 
    sum(y[k, (i, j)] for (i, j) in keys(filtered_Ty)) <= 1
)

#Trucks can only travel if they first leave from a factory 
@constraint(model, [k=1:S], 
    sum(x[k, (j1, j2)] for (j1, j2) in keys(filtered_Tx)) <= (N - 1) * sum(y[k, (i, j)] for (i, j) in keys(filtered_Ty))
)

#Trucks can only leave used factories
# @constraint(model, [i=1:M], sum(y[k, (i, j)] for k in 1:S, j in 1:N) <= S * o[i])
@constraint(model, [i=1:M], 
    sum(y[k, (i, j)] for k in 1:S, (f, j) in keys(filtered_Ty) if i == f) <= S * o[i]
)

#Trucks start and end at the same factory
@constraint(model, [k=1:S, i=1:M],
    sum(z[k, (j, i)] for (j, f) in keys(filtered_Tz)if f == i) ==
    sum(y[k, (i, j)] for (f, j) in keys(filtered_Ty) if f == i)
)

println("Finished Factory Constraints")



#FLOW CONSTRAINTS
#SUM IN = 1
function edges_end_at(edges, end_node)
    return [(x, y) for (x, y) in keys(edges) if y == end_node]
end
function edges_start_at(edges, start_node)
    return [(x, y) for (x, y) in keys(edges) if x == start_node]
end

ends_at_dict_Tx = Dict(j2 => edges_end_at(filtered_Tx, j2) for j2 in 1:N)
ends_at_dict_Ty = Dict(j2 => edges_end_at(filtered_Ty, j2) for j2 in 1:N)

@constraint(model, [j2=1:N], 
    sum(
        sum(y[k, (i, j2)] for (i, j) in ends_at_dict_Ty[j2]) +
        sum(x[k, (j1, j2)] for (j1, dem) in ends_at_dict_Tx[j2]) 
        for k in 1:S
    ) == 1
)
# @constraint(model, [j2=1:N], 
#     sum(
#         sum(y[k, (i, j2)] for (i, j) in keys(filtered_Ty) if j == j2) +
#         sum(x[k, (j1, j2)] for (j1, dem) in keys(filtered_Tx) if dem == j2) 
#         for k in 1:S
#     ) == 1
# )

println("Finished Flow In Constraints")
#If truck k enters location j, it must exit location j

# @constraint(model, [j=1:N, k=1:S],
#     (sum(y[k, (i, j)] for i in 1:M) + sum(x[k, (j1, j)] for j1 in 1:N)) == 
#     (sum(x[k, (j, j2)] for j2 in 1:N) + sum(z[k, (j, i)] for i in 1:M))
# )

starts_at_dict_Tx = Dict(j1 => edges_start_at(filtered_Tx, j1) for j1 in 1:N)
starts_at_dict_Tz = Dict(j => edges_start_at(filtered_Tz, j) for j in 1:N)

@constraint(model, [j=1:N, k=1:S], (sum(y[k, (i, j)] for (i,j) in ends_at_dict_Ty[j]) + 
                                    sum(x[k, (j1, j)] for (j1,j) in ends_at_dict_Tx[j])) == 
                                    (sum(x[k, (j, j2)] for (j,j2) in starts_at_dict_Tx[j]) + 
                                    sum(z[k, (j, i)] for (j,i) in starts_at_dict_Tz[j])))

# @constraint(model, [j=1:N, k=1:S],
#     (sum(y[k, (i, j)] for i in 1:M if (i, j) in keys(filtered_Ty)) + 
#      sum(x[k, (j1, j)] for j1 in 1:N if (j1, j) in keys(filtered_Tx))) == 
#     (sum(x[k, (j, j2)] for j2 in 1:N if (j, j2) in keys(filtered_Tx)) + 
#      sum(z[k, (j, i)] for i in 1:M if (j, i) in keys(filtered_Tz)))
# )

println("Finished Flow Constraints")
# Time constraints

@constraint(model, [k=1:S], 
    f[k] == 
    sum(y[k, (i, j)] * Ty[i, j] for (i, j) in keys(filtered_Ty)) +
    sum(x[k, (j1, j2)] * Tx[j1, j2] for (j1, j2) in keys(filtered_Tx))
    )

@constraint(model, [k=1:S], f[k] <= L)

optimize!(model)

println(sum(value.(o)))

# println()
# try
#     rm("results/output.h5")
# catch
#     1
# end
# h5write("results/output.h5", "factories", value.(o))
# h5write("results/output.h5", "x_edges", value.(x))
# h5write("results/output.h5", "y_edges", value.(y))
# h5write("results/output.h5", "z_edges", value.(z))
