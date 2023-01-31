package utils

import "container/heap"

func MinimumEditDistance(token1, token2 string) int {
	dp := make([][]int8, len(token1)+1)
	for i := range dp {
		dp[i] = make([]int8, len(token2)+1)
		dp[i][0] = int8(i)
	}
	for i := range dp[0] {
		dp[0][i] = int8(i)
	}
	for i := 1; i <= len(token1); i++ {
		for j := 1; j <= len(token2); j++ {
			if token1[i-1] == token2[j-1] {
				dp[i][j] = dp[i-1][j-1]
				continue
			}
			dp[i][j] = Min8(dp[i-1][j-1], dp[i-1][j], dp[i][j-1]) + 1
		}
	}
	return int(dp[len(token1)][len(token2)])
}

func TopNMostSimilar(n int, token string, dictionary []string) *[][2]int {

	h := NewTheHeap(n)
	for i := range dictionary {
		distance := MinimumEditDistance(token, dictionary[i])
		heap.Push(h, HeapItem{Index: i, Distance: distance})
	}
	result := make([][2]int, n)
	for i := range result {
		temp := heap.Pop(h).(HeapItem)
		result[i] = [2]int{temp.Index, temp.Distance}
	}
	return &result
}
