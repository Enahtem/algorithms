numbers = [1,2,7,1,3,6]

def merge(nums1, nums2):
    nums = []
    while nums1 and nums2:
        if nums1[0] < nums2[0]:
            nums.append(nums1.pop(0))
        else:
            nums.append(nums2.pop(0))
    if nums1:
        return nums+nums1
    elif nums2:
        return nums+nums2
    else:
        return nums

def merge_sort(numbers):
    halfway = len(numbers)//2
    if halfway==0:
        return numbers
    return merge(merge_sort(numbers[:halfway]), merge_sort(numbers[halfway:]))


print(merge_sort(numbers))
