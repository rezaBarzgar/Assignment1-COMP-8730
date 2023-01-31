package main

import (
	"fmt"
	"log"
	"nlp/assignment1/utils"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

const (
	MaxK = 15
)

type tokenPair struct {
	token        string
	correctToken string
	successMask  int64
}

func main() {

	wn, err := utils.ReadDat("data/wn.dat")
	if err != nil {
		log.Fatal(err)
	}
	miss, err := utils.ReadDat("data/missp.dat")
	if err != nil {
		log.Fatal(err)
	}

	const NumberOfJobs = 10
	args := make(chan tokenPair, NumberOfJobs)
	results := make(chan tokenPair, NumberOfJobs)

	wg := new(sync.WaitGroup)

	for i := 0; i < NumberOfJobs; i++ {
		wg.Add(1)
		go worker(args, results, wn, wg)
	}

	pairs := []tokenPair{}
	currentCorrectToken := ""
	start := time.Now()
	for i := range miss {
		if miss[i][0] == '$' {
			currentCorrectToken = miss[i][1:]
		} else {
			pairs = append(pairs, tokenPair{
				token:        miss[i],
				correctToken: currentCorrectToken,
			})
		}
	}
	go func() {
		for i := range pairs {
			args <- pairs[i]
		}
		close(args)
	}()
	go func() {
		wg.Wait()
		close(results)
	}()
	total, top1, top5, top10 := 0, 0, 0, 0
	var stringBuilder strings.Builder
	for result := range results {
		if result.successMask&(1<<1) > 0 {
			top1 += 1
			top5 += 1
			top10 += 1
		} else if result.successMask&(1<<5) > 0 {
			top5 += 1
			top10 += 1
		} else if result.successMask&(1<<10) > 0 {
			top10 += 1
		}
		_, err := stringBuilder.WriteString(fmt.Sprintf("%s,%s,%s,%d\n", result.token, result.correctToken, strconv.FormatInt(result.successMask, 2), result.successMask))
		if err != nil {
			fmt.Println(err)
		}
		total += 1
		if total%50 == 0 {
			fmt.Println(total)
		}
	}
	end := time.Now()
	err = os.WriteFile("data/output.dat", []byte(stringBuilder.String()), 0644)
	if err != nil {
		log.Fatalln(err)
	}
	fmt.Println(float64(top1) / float64(total))
	fmt.Println(float64(top5) / float64(total))
	fmt.Println(float64(top10) / float64(total))
	fmt.Println(end.UnixMilli() - start.UnixMilli())
	wg.Wait()

}

func worker(tokenPairs <-chan tokenPair, results chan<- tokenPair, dictionary []string, wg *sync.WaitGroup) {
	defer wg.Done()
	for pair := range tokenPairs {
		topk := utils.TopNMostSimilar(MaxK, pair.token, dictionary)
		temp := int64(0)
		for i := range *topk {
			if dictionary[(*topk)[i][0]] == pair.correctToken {
				temp = temp | (1 << i)
			}
		}
		pair.successMask = temp
		results <- pair
	}

}
