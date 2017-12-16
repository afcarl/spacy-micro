package spacy

import (
	"encoding/json"
	"net/http"
	"bytes"
	"strconv"
	"log"
)

// post a request to the parser server (spacy)
func postRequest(url string, text string) string {
	req, err := http.NewRequest("POST", url, bytes.NewBufferString(text))
	req.Header.Set("Content-Type", "text/plain")
	cl := strconv.Itoa(len(text))
	req.Header.Set("Content-Length", cl)
	client := &http.Client{}
	response, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
		panic(err)
	}
	defer response.Body.Close()
	buf := new(bytes.Buffer)
	buf.ReadFrom(response.Body)
	return buf.String()
}

// parse a piece of text and return the list of sentences parsed by spaCy
// serviceAddress:  the spacy endpoint, e.g. "http://localhost:9000/parse"
// text: the text to parse
func ParseText(serviceAddress string, text string) string {
	return postRequest(serviceAddress, text)
}
