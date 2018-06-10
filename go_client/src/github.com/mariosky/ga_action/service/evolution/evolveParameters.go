package evolution

// Evolution parameters data type definition.
type Problem struct {
	Name string `json:"name"`
	Function int `json:"function"`
	Instance int `json:"instance"`
	SearchSpace []int `json:"search_space"`
	Dim int `json:"dim"`
	Error float64 `json:"error"`
}

type Experiment struct {
	ExperimentID string `json:"experiment_id"`
	Owner string `json:"owner"`
	Type string `json:"type"`
}

type Selection struct {
	Type string `json:"type"`
	Tournsize int `json:"tournsize"`
}

type Crossover struct {
	Type string`json:"type"`
	CXPB []float64`json:"CXPB"`
}

type Mutation struct {
	Type string`json:"type"`
	Mu int`json:"mu"`
	Sigma float64`json:"sigma"`
	Indpb float64`json:"indpb"`
	MUTPB float64`json:"MUTPB"`
}

type Algorithm struct {
	Name string`json:"name"`
	Iterations int`json:"iterations"`
	Selection Selection`json:"selection"`
	Crossover Crossover`json:"crossover"`
	Mutation Mutation`json:"mutation"`
}

type EvolveParameters struct {
	ID string`json:"id"`
	Problem Problem`json:"problem"`
	Population []CreatedSample`json:"population"`
	PopulationSize int`json:"population_size"`
	Experiment Experiment`json:"experiment"`
	Algorithm Algorithm`json:"algorithm"`
}
