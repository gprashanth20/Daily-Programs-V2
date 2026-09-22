public class StackUsingArray {
    private final int[] data;
    private int top = -1;

    public StackUsingArray(int capacity) {
        data = new int[capacity];
    }

    public void push(int value) {
        if (top == data.length - 1) throw new RuntimeException("Stack overflow");
        data[++top] = value;
    }

    public int pop() {
        if (top == -1) throw new RuntimeException("Stack underflow");
        return data[top--];
    }

    public boolean isEmpty() { return top == -1; }

    public static void main(String[] args) {
        StackUsingArray stack = new StackUsingArray(5);
        stack.push(1);
        stack.push(2);
        stack.push(3);
        while (!stack.isEmpty()) {
            System.out.println(stack.pop());
        }
    }
}
