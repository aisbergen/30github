class Solution {
    public int removeDuplicates(int[] nums) {
        int j=0;
        for(int i=0; i<nums.length; i++){
            nums[j]=nums[i];
            if(j<2 || nums[i]!=nums[j-2]){
                nums[j]=nums[i];
                j++;
            }
        }
        return j;
    }
}