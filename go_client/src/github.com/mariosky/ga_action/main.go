package main

import "fmt"
import "encoding/json"
import "./service/evolution"
import "./util"
import "./configuration"

func createIds(settings configuration.Configuration, createdIds chan string) {
	for i := 0; i < settings.Requests; i++ {
		util.Log(settings, "Creating...")
		id, err := evolution.IdNewPopulation(settings)
		if err != nil {
			fmt.Println(err)
		} else {
			createdIds <- id
		}
	}
}

func create(settings configuration.Configuration,
	createdIds chan string,
	created chan []evolution.CreatedSample) {
	for {
		util.Log(settings, "Fetching created...")
		pop, err:= evolution.GetNewPopulation(settings, <-createdIds)
		if err != nil {
			fmt.Println(err)
		} else {
			created <- pop
		}
	}
}
func evolveIds(settings configuration.Configuration,
	created chan []evolution.CreatedSample,
	evolvedIds chan string) {
	for i := 0; i < settings.Requests * settings.Iterations; i++ {
		util.Log(settings, "Evolving...")
		parameters, err := evolution.CreateEvolveParameters(
			settings, <-created)
		if err != nil {
			fmt.Println(err)
		}

		id, err := evolution.IdEvolve(settings, parameters)
		if err != nil {
			fmt.Println(err)
		} else {
			evolvedIds <- id
		}
	}
}

func evolve(settings configuration.Configuration,
	evolvedIds chan string,
	evolved chan evolution.EvolveResponse,
	created chan []evolution.CreatedSample) {
	for {
		util.Log(settings, "Fetching evolved...")
		res, err := evolution.GetEvolve(settings, <-evolvedIds)
		if err != nil {
			fmt.Println(err)
		} else {
			evolved <- res
		}
	}
}

func crossoverMigration(settings configuration.Configuration,
	evolved chan evolution.EvolveResponse,
	created chan []evolution.CreatedSample,
	migrated chan evolution.EvolveResponse) {
	var pop_a *evolution.EvolveResponse = nil
	var pop_b *evolution.EvolveResponse = nil
	for {
		util.Log(settings, "Migrating...")
		if pop_a == nil {
			pop := <-evolved
			pop_a = &pop
		}
		if pop_b == nil {
			pop_b = pop_a
		} else {
			pop := <-evolved
			pop_b = &pop
		}
		evolution.CrossoverMigration((*pop_a).Population, (*pop_b).Population)

		samples := make([]evolution.CreatedSample, len((*pop_a).Population))
		for key, value := range (*pop_a).Population {
			samples[key] = evolution.CreatedSample{
				ID: value.ID,
				Chromosome: value.Chromosome,
				Fitness: evolution.CreatedFitness{
					DefaultContext: value.Fitness.DefaultContext,
				},
			}
		}
		migrated <- *pop_a
		go func() {
			created <- samples
		}()
	}
}

func printEvolved(settings configuration.Configuration,
	migrated chan evolution.EvolveResponse) {
	for i := 0; i < settings.Requests * settings.Iterations; i++ {
		pop, ok := <-migrated
		if ok {
			popJson, err := json.Marshal(pop)
			if err == nil {
				fmt.Printf("%+v\n", string(popJson))
			}
		}
	}
}

func main() {
	var settings = configuration.Settings
	var createdIds = make(chan string)
	var created = make(chan []evolution.CreatedSample)
	var evolvedIds = make(chan string)
	var evolved = make(chan evolution.EvolveResponse)
	var migrated = make(chan evolution.EvolveResponse)

	go createIds(settings, createdIds)
	go create(settings, createdIds, created)
	go evolveIds(settings, created, evolvedIds)
	go evolve(settings, evolvedIds, evolved, created)
	go crossoverMigration(settings, evolved, created, migrated)
	printEvolved(settings, migrated)
}
