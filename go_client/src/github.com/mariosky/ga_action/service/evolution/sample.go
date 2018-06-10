package evolution

// Sample data type definition.
type EvaluatedFitness struct {
	DefaultContext float64`json:"DefaultContext"`
	Score float64`json:"score"`
}

type EvaluatedSample struct {
	ID string`json:"id"`
	Chromosome []float64`json:"chromosome"`
	Fitness EvaluatedFitness`json:"fitness"`
}

type SortEvaluatedSample [] EvaluatedSample
func (samples SortEvaluatedSample) Len() int {
	return len(samples)
}
func (samples SortEvaluatedSample) Less(i,  j int) bool {
	return samples[i].Fitness.Score <
		samples[j].Fitness.Score
}
func (samples SortEvaluatedSample) Swap(i, j int) {
	sample := samples[i]
	samples[i] = samples[j]
	samples[j] = sample
}

// The math libary doesn't have a min function for integers.
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

// Population type.
type CreatedFitness struct {
	DefaultContext float64`json:"DefaultContext"`
}

type CreatedSample struct {
	ID string`json:"id"`
	Fitness CreatedFitness `json:"fitness"`
	Chromosome []float64`json:"chromosome"`
}
