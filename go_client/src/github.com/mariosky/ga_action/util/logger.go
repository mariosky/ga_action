package util

import "fmt"
import "../configuration"

func Log(settings configuration.Configuration, message string)  {
	if (settings.Verbose) {
		fmt.Println(message)
	}
}
