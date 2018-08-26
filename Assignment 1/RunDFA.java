//usage after compilation: java RunDFA 0101010101011111000101
public class RunDFA {
    public static void main(String[] args) {
        String string = args[0].toString();
        int state = 0;
        for (char c : string.toCharArray()) {
            switch (state) {
                case (0): {
                    if (c == '0') {
                        state = 1;
                    } else if (c == '1') {
                        state = 3;
                    }
                }
                break;
                case (1): {
                    if (c == '0' || c == '1') {
                        state = 2;
                    }
                }
                break;
                case (2): {
                    if (c == '0' || c == '1') {
                        state = 2;
                    }
                }
                break;
                case (3): {
                    if (c == '0') {
                        state = 3;
                    } else if (c == '1') {
                        state = 4;
                    }
                }
                break;
                case (4): {
                    if (c == '0') {
                        state = 4;
                    } else if (c == '1') {
                        state = 5;
                    }
                }
                break;
                case (5): {
                    if (c == '0' || c == '1') {
                        state = 2;
                    }
                }
                break;
            }
        }
        if (state == 2 || state == 5) {
            System.out.println("Yes.");
        } else {
            System.out.println("No.");
        }
    }
}
