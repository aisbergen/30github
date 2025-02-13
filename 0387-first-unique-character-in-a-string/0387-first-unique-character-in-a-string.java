class Solution {
    public int firstUniqChar(String s) {
        int[] freq = new int [26];
        int len = s.length();
        for (int i=0; i<len; i++ ){
            char num = s.charAt(i);
            freq[num - 'a']++;
            }
        
        for (int i=0; i<len; i++){
                if (freq[s.charAt(i) - 'a'] == 1 ){
                return i ;
            }
        }
            
        
        return -1;
            
        } 

        
    }
