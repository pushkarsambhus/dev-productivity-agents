class slidingWindow:
    def maxProfit(self, prices):
        # Your code here
        min_price = prices[0]
        max_profit = 0
        profit = 0

        for price in prices:
            if price < min_price:
                min_price = price

            profit = price - min_price

            if profit > max_profit:
                max_profit = profit


        return max(max_profit,profit)



if __name__ == "__main__":
    sol = slidingWindow()

    #print(sol.maxProfit([7, 1, 5, 3, 6, 4]))  # 5
    #print(sol.maxProfit([7, 6, 4, 3, 1]))  # 0
    print(sol.maxProfit([2, 4, 1, 7, 5, 11]))  # 9