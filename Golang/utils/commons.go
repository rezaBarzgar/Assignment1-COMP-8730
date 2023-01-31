package utils

import (
	"fmt"
	"log"
	"os"
	"strings"
)

func ReadDat(path string) ([]string, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		log.Fatal(err)
	}
	_ = data
	rawList := strings.ToLower(string(data))
	result := strings.Split(rawList, "\r\n")
	return result, nil
}

func Min8(numbers ...int8) int8 {
	if len(numbers) == 0 {
		fmt.Println("SHIT AT min8")
		return 0
	}
	result := numbers[0]
	for i := 1; i < len(numbers); i++ {
		if numbers[i] < result {
			result = numbers[i]
		}
	}
	return result
}
