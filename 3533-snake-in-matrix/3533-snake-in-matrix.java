class Solution {
    public int finalPositionOfSnake(int n, List<String> commands) {
        int number =0;
        for(String command : commands){
            if(command.equals("UP")){
            number -=n;
            } else if (command.equals("DOWN")){
            number +=n;
            } else if (command.equals("RIGHT")){
            number++;
            } else if (command.equals("LEFT")){
            number--;
            }
        }
        return number;
    }
}        