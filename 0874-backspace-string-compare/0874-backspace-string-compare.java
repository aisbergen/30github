class Solution {
    public boolean backspaceCompare(String s, String t) {
        return build(s).equals(build(t));
    }
    
    private String build(String str) {
        StringBuilder builtStr = new StringBuilder();
        for (char c : str.toCharArray()) {
            if (c != '#') { // If it's not a backspace char, append it.
                builtStr.append(c);
            } else { // If it's backspace char, then..
                if (builtStr.length() != 0) {  // if the builtStr isn't empty.. 
                    builtStr.deleteCharAt(builtStr.length() - 1); // remove last char.
                }
            }
        }
        return builtStr.toString();
    }
}