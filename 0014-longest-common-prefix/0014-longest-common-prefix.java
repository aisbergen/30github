class Solution {
    public String longestCommonPrefix(String[] strs) {
        String prefix = strs[0];
        for (int i=1; i<strs.length; i++ ){
            String word = strs[i];
            while(!word.startsWith(prefix)){
               prefix = prefix.substring(0, prefix.length() - 1);
            }
            if(prefix.equals("")){
                return "";
            }
        }
        return prefix;
    }
}