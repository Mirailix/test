# rating = [120, 90, 150, 110]
# rating.append(130)      # [120, 90, 150, 110, 130]
# last_player = rating.pop()   # last_player = 130, rating = [120, 90, 150, 110]
# print(sorted(rating))           # [90, 110, 120, 150]
# print(rating)

class Solution(object):

    def twoSum(self,nums,target):
        for i in range (len(nums)):
            if(nums[i]<=target or nums[i]>=target):
                n=nums[i]
                for j in range (len(nums)):
                    if j==i:
                        continue
                    if n+nums[j]==target:
                        return [i,j]
                    
class Solution(object):

    def twoSum(self,nums,target):
        seen={}
        for i in range (len(nums)):
            diff=target-nums[i]
            if diff in seen:
                return [seen[diff],i]
            else:
                seen[nums[i]]=i
