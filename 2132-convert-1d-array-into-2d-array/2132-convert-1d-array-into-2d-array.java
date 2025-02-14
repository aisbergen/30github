class Solution {
    public int[][] construct2DArray(int[] original, int m, int n) {
        int index =0;
        if (m * n != original.length){
            return new int[0][0];
        }
        int[][] result = new int[m][n];
        for (int i=0; i<m; i++){
            for (int j=0; j<n; j++){
                result[i][j] = original[index];
                index++;

            }
        }
        return result;
    }
}