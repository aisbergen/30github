class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
    List<Integer> result = new ArrayList<>();
    int top = 0;
    int bottom = matrix.length - 1;
    int left = 0;
    int right = matrix[0].length - 1;
    while (top <= bottom && left <= right){
        for (int i=left; i<=right; i++){
            result.add(matrix[top][i]); //left to right (top row)
        }
        top++; //move boundary down
        for(int i=top; i<=bottom; i++){ 
            result.add(matrix[i][right]); // top - bottom (right column)
        }
        right--; //move right boundary left
        
        if(top<=bottom){
            for(int i=right; i>=left; i--){
                result.add(matrix[bottom][i]);
            }
            bottom--; //move boundary up
        }

        if(left<=right){
            for(int i=bottom; i>=top; i--){
                result.add(matrix[i][left]);
            }
            left++; //move boundary right
        }

    }

    return result;

    }
}