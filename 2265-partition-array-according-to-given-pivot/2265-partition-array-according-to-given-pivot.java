class Solution {
    public int[] pivotArray(int[] nums, int pivot) {
        ArrayList<Integer> small = new ArrayList<>();
        ArrayList<Integer> equal = new ArrayList<>();
        ArrayList<Integer> large = new ArrayList<>();
        int index=0;
        for(int i=0; i<nums.length; i++){
            if(nums[i]<pivot){
                small.add(nums[i]);
            }
            if(nums[i]>pivot){
                large.add(nums[i]);
            }
            if(nums[i]==pivot){
                equal.add(nums[i]);
            }   
        }
        for (int num : small){ 
            nums[index++] = num;}
        for (int num : equal){ 
            nums[index++] = num;}
        for (int num : large){ 
            nums[index++] = num;}
        return nums;
    }
}