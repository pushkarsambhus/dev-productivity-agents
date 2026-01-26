def solution(numbers):
    # TODO: Implement solution here
    n = len(numbers)
    result = []
    
    for i in range(((n+1)//2)):
        result.append(numbers[i] + numbers[n-1-i])
    
    print(result)
    return result
        
    
             
    pass