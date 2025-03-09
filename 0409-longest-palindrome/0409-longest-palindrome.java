class Solution {
    public int longestPalindrome(String s) {
        if (s == null || s.length()==0){
            return 0;
        }
        HashSet<Character> hash_set = new HashSet<Character>();
        int pal_length = 0;
        for (char ch: s.toCharArray()){
            if(hash_set.contains(ch)){
                hash_set.remove(ch);
                pal_length +=2;
            }
            else{
                hash_set.add(ch);
            }
            
        }
        if(!hash_set.isEmpty()){
            pal_length++;
        }
        return pal_length;
}}
