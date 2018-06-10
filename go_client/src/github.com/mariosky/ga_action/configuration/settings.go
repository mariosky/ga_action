package configuration

import "flag"
import "os"
import "strconv"

// Settings data type
type Configuration struct {
	Verbose bool `json:"verbose"`
	Log bool `json:"log"` // todo
	Blocking bool `json:"blocking"` // todo
	Requests int `json:"requests"`
	OnlyPopulation bool `json:"only_population"` // todo
	Timeout int `json:"timeout"` // todo
	Apihost string `json:"apihost"`
	Namespace string `json:"namespace"`
	Auth string `json:"authorization"` // todo
	Insecure bool `json:"insecure"` // todo
	Function int `json:"function"`
	Instance int `json:"instance"`
	Dim int `json:"dim"`
	PopulationSize int `json:"population_size"`
	Iterations int `json:"iterations"`
}

var Settings Configuration

func init() {
	function, err := strconv.Atoi(os.Getenv("FUNCTION"))
	if err != nil {
		function = 3
	}

	instance, err:= strconv.Atoi(os.Getenv("INSTANCE"))
	if err != nil {
		instance =  1
	}

	dim, err := strconv.Atoi(os.Getenv("DIM"))
	if err != nil {
		dim = 3
	}

	populationSize, err:= strconv.Atoi(os.Getenv("POPULATION_SIZE"))
	if err != nil {
		populationSize = 20
	}

	verbosePointer := flag.Bool("verbose",  false,  "verbose output")
	logPointer := flag.Bool("log",  false,  "log to redis")
	blockingPointer := flag.Bool("blocking", false,  "blocking")
	requestsPointer := flag.Int("requests", 2, "number of requests (default 2)")
	onlyPopulationPointer := flag.Bool("only-population",  false, "return only population")
	timeoutPointer := flag.Int("timeout", 60, "seconds for timeout (default 60)")
	apihostPointer := flag.String("apihost", os.Getenv("APIHOST"), "whisk API HOST (default $APIHOST)")
	namespacePointer := flag.String("namespace", os.Getenv("NAMESPACE"), "whisk NAMESPACE (default $NAMESPACE)")
	authPointer := flag.String("auth", os.Getenv("AUTH"), "authorization KEY (default wsk property)")
	insecurePointer := flag.Bool("insecure",  false,  "bypass certificate checking")
	functionPointer := flag.Int("function", function, "(default $FUNCTION or 3)")
	instancePointer := flag.Int("instance", instance, "(default $INSTANCE or 1)")
	dimPointer := flag.Int("dim", dim, "(default $DIM or 3)")
	populationSizePointer := flag.Int("population-size", populationSize, "population size (default $POPULATION_SIZE or 20)")
	iterationsPointer := flag.Int("iterations", 1, "iterations over population")

	flag.Parse()
	Settings = Configuration{
		Verbose: *verbosePointer,
		Log: *logPointer,
		Blocking: *blockingPointer,
		Requests: *requestsPointer,
		OnlyPopulation: *onlyPopulationPointer,
		Timeout: *timeoutPointer,
		Apihost: *apihostPointer,
		Namespace: *namespacePointer,
		Auth: *authPointer,
		Insecure: *insecurePointer,
		Function: *functionPointer,
		Instance: *instancePointer,
		Dim: *dimPointer,
		PopulationSize: *populationSizePointer,
		Iterations: *iterationsPointer,
	}
}
