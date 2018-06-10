package whisk

import "text/template"
import "bytes"
import "net/http"
import "crypto/tls"
import "net/url"
// ximport "io/ioutil"
import "encoding/json"
import "time"

var transport = &http.Transport{
	TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
}
var client = &http.Client{Timeout: 30 * time.Second, Transport: transport,}

var rest, err = template.
	New("rest").
	Parse("{{.Apihost}}/api/v1/namespaces/{{.Namespace}}/{{.Endpoint}}/{{.Value}}")

type User struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

type WhiskApi struct {
	Apihost string `json:"apihost"`
	Namespace string `json:"namespace"`
}

type WhiskRequestData struct {
	Json interface{} `json:"json"`
	Verify bool `json:"verify"`
	User User `json:"user"`
}

type whiskApiRequest struct {
	Apihost string `json:"apihost"`
	Namespace string `json:"namespace"`
	Endpoint string `json:"endpoint"`
	Value string `json:"value"`
}

func (api WhiskApi) RequestUrl(endpoint, value string,
	data map[string]interface{}) (string, error) {
	apiReq := whiskApiRequest{
		api.Apihost,
		api.Namespace,
		endpoint,
		value,
	}
	var urlBytes bytes.Buffer
	err := rest.Execute(&urlBytes, apiReq)
	if err != nil {
		return "", err
	}

	urlObj, err := url.Parse(urlBytes.String())
	if err != nil {
		return "", err
	}

	queryObj := urlObj.Query()
	queryObj.Add("blocking", "false")
	queryObj.Add("result", "true")
	for k, v := range data {
		queryObj.Add(k, v.(string))
	}
	urlObj.RawQuery  = queryObj.Encode()

	return urlObj.String(), err
}

type ActionResponse struct {
	ActivationId string `json:"activationId"`
}

func (api WhiskApi) Action(action string, data WhiskRequestData,
	target *ActionResponse) error {
	urlString, err := api.RequestUrl("actions", action,
		map[string]interface{}{})
	if err != nil {
		return err
	}

	jsonBytes, err := json.Marshal(data.Json)
	if err != nil {
		return err
	}

	req, err := http.NewRequest(
		"POST",
		urlString,
		bytes.NewBuffer(jsonBytes),
	)
	if err != nil {
		return err
	}

	req.Header.Set("Content-Type", "application/json")
	req.SetBasicAuth(data.User.Username, data.User.Password)

	res, err := client.Do(req)
	if err != nil {
		return err
	}

	defer res.Body.Close()

	err = json.NewDecoder(res.Body).Decode(&target)
	if err != nil {
		return err
	}

	return nil
}

type ActivationValue struct {
	Value string `json:"value"`
}

type ActivationResult struct {
	Result ActivationValue `json:"result"`
}

type ActivationResponse struct {
	Response ActivationResult `json:"response"`
}

func (api WhiskApi) Activation(data WhiskRequestData,
	target *ActivationResponse) error {
	urlString, err := api.RequestUrl("activations",
		data.Json.(ActionResponse).ActivationId,
		map[string]interface{}{})
	if err != nil {
		return err
	}

	req, err := http.NewRequest(
		"GET",
		urlString,
		nil,
	)
	if err != nil {
		return err
	}

	req.Header.Set("Content-Type", "application/json")
	req.SetBasicAuth(data.User.Username, data.User.Password)

	res, err := client.Do(req)
	if err != nil {
		return err
	}

	defer res.Body.Close()

	err = json.NewDecoder(res.Body).Decode(&target)
	if err != nil {
		return err
	}

	return nil
}
