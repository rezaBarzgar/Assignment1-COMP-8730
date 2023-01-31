package utils

import (
	"container/heap"
)

func NewTheHeap(MaxLength int) *TheHeap {
	h := &TheHeap{
		MaxLength: MaxLength,
	}
	h.Items = &[]HeapItem{}
	heap.Init(h)
	return h
}

type HeapItem struct {
	Index    int
	Distance int
}

type TheHeap struct {
	Items     *[]HeapItem
	MaxLength int
}

func (h TheHeap) Len() int { return len(*h.Items) }

func (h TheHeap) Less(i, j int) bool {
	return (*h.Items)[i].Distance <= (*h.Items)[j].Distance
}
func (h TheHeap) Swap(i, j int) {
	(*h.Items)[i].Index, (*h.Items)[j].Index = (*h.Items)[j].Index, (*h.Items)[i].Index
	(*h.Items)[i].Distance, (*h.Items)[j].Distance = (*h.Items)[j].Distance, (*h.Items)[i].Distance
}

func (h *TheHeap) Push(x any) {
	*(*h).Items = append((*(*h).Items), x.(HeapItem))
}

func (h *TheHeap) Pop() any {
	old := *(*h).Items
	n := len(*(*h).Items)
	x := old[n-1]
	*(*h).Items = old[0 : n-1]
	return x
}
