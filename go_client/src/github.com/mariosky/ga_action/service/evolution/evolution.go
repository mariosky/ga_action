package evolution

import "encoding/json"
import "sort"
import "github.com/satori/go.uuid"
import "../whisk"
import "../../configuration"

func evolutionParameters(function int, instance int, dim int,
	populationSize int) (EvolveParameters, error) {
	var id, err = uuid.NewV1()
	return EvolveParameters{
		ID: id.String(),
		Problem: Problem{
			Name: "BBOB",
			Function: function,
			Instance: instance,
			SearchSpace: []int {-5, 5},
			Dim: dim,
			Error: 1e-8,
		},
		Population: []CreatedSample{},
		PopulationSize: populationSize,
		Experiment: Experiment{
			ExperimentID: "dc74efeb-9d64-11e7-a2bd-54e43af0c111",
			Owner: "mariosky",
			Type: "benchmark",
		},
		Algorithm: Algorithm{
			Name: "GA",
			Iterations: 5,
			Selection: Selection{
				Type: "tools.selTournament",
				Tournsize: 12,
			},
			Crossover: Crossover{
				Type: "cxTwoPoint",
				CXPB: []float64 {0, 0.2},
			},
			Mutation: Mutation{
				Type: "mutGaussian",
				Mu: 0,
				Sigma: 0.5,
				Indpb : 0.05,
				MUTPB: 0.5,
			},
		},
	},  err
}

func CreateEvolveParameters(settings configuration.Configuration,
	population []CreatedSample) (EvolveParameters, error) {
	parameters, err :=  evolutionParameters(
		settings.Function,
		settings.Instance,
		settings.Dim,
		settings.PopulationSize,
	)
	parameters.Population = population
	return parameters, err
}

func IdNewPopulation(settings configuration.Configuration) (string, error) {
	var whiskApi = whisk.WhiskApi{ settings.Apihost, settings.Namespace }
	var res whisk.ActionResponse
	err := whiskApi.Action("popService", whisk.WhiskRequestData{
		Json: CreatePopulationParameters{
			PopulationSize: settings.PopulationSize,
			Problem: CreatePopulationProblem{
				Dim: settings.Dim,
			},
		},
		Verify: false,
		User: whisk.User{
			Username: "admin",
			Password: "secret",
		},
	}, &res)

	return res.ActivationId, err
}

func GetNewPopulation(settings configuration.Configuration,
	id string) ([]CreatedSample, error) {
	var whiskApi = whisk.WhiskApi{ settings.Apihost, settings.Namespace }
	var res whisk.ActivationResponse
	err := whiskApi.Activation(whisk.WhiskRequestData{
		Json: whisk.ActionResponse{id},
		Verify: false,
		User: whisk.User{
			Username: "admin",
			Password: "secret",
		},
	}, &res)

	value := []byte(res.Response.Result.Value)
	var samples []CreatedSample
	err = json.Unmarshal(value, &samples)
	if err != nil {
		return nil, err
	}

	return samples, err
}

func IdEvolve(settings configuration.Configuration,
	params EvolveParameters) (string, error) {
	var whiskApi = whisk.WhiskApi{ settings.Apihost, settings.Namespace }
	var res whisk.ActionResponse
	err := whiskApi.Action("gaService", whisk.WhiskRequestData{
		Json: params,
		Verify: false,
		User: whisk.User{
			Username: "admin",
			Password: "secret",
		},
	}, &res)

	return res.ActivationId, err
}

func GetEvolve(settings configuration.Configuration,
	id string) (EvolveResponse, error) {
	var whiskApi = whisk.WhiskApi{ settings.Apihost, settings.Namespace }
	var res whisk.ActivationResponse
	err := whiskApi.Activation(whisk.WhiskRequestData{
		Json: whisk.ActionResponse{id},
		Verify: false,
		User: whisk.User{
			Username: "admin",
			Password: "secret",
		},
	}, &res)

	value := []byte(res.Response.Result.Value)
	var evolveResponse EvolveResponse
	err = json.Unmarshal(value, &evolveResponse)
	if err != nil {
		return evolveResponse, err
	}

	return evolveResponse, err
}

func CrossoverMigration(populationA SortEvaluatedSample,
	populationB SortEvaluatedSample) {
	sort.Sort(&populationA)
	sort.Sort(&populationB)
	size := min(len(populationA),  len(populationB))
	cxPoint :=  int(size / 2)
	copy(populationA,
		append(populationA[: cxPoint],
			populationB[:cxPoint + size % 2]...))
}
