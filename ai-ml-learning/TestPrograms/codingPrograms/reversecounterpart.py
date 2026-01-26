def solution(numbers):
    # TODO: implement solution here
    reverse_counterpart = []
    lookup_set = set(numbers)
    
    for n in numbers:    
        if(len(str(n)) == 1 ):
            reverse_counterpart.append((n,n))
        else:
            numstr = str(n)
            numstr = numstr[::-1]
            if int(numstr) in lookup_set:
                reverse_counterpart.append((n,int(numstr)))
    
    print(reverse_counterpart)
                
    return reverse_counterpart