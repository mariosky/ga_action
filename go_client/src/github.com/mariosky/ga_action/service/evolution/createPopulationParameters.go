package evolution

// Create population parameters data types.
type CreatePopulationProblem struct {
	Dim int`json:"dim"`
}

type CreatePopulationParameters struct {
	PopulationSize int`json:"population_size"`
	Problem CreatePopulationProblem`json:"problem"`
}
