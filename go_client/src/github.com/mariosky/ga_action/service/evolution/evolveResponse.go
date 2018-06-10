package evolution

type ProblemResponse struct {
	Function int`json:"function"`
	Dim int`json:"dim"`
	Name string`json:"name"`
	SearchSpace []int`json:"search_space"`
	Instance int`json:"instance"`
	Error float64`json:"error"`
}

type EvolveResponse struct {
	Fopt float64`json:"fopt"`
	Algorithm Algorithm`json:"algorithm"`
	BestIndividual []float64`json:"best_individual"`
	Experiment Experiment`json:"experiment"`
	PopulationSize int`json:"population_size"`
	Iterations [][]interface{}`json:"iterations"`
	Problem ProblemResponse`json:"problem"`
	ID string`json:"id"`
	Best bool`json:"best"`
	Population []EvaluatedSample`json:"population"`
}
