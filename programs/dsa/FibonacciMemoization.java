import java.util.HashMap;
import java.util.Map;

public class FibonacciMemoization {
    static final Map<Integer, Long> memo = new HashMap<>();

    static long fib(int n) {
        if (n <= 1) return n;
        if (memo.containsKey(n)) return memo.get(n);
        long result = fib(n - 1) + fib(n - 2);
        memo.put(n, result);
        return result;
    }

    public static void main(String[] args) {
        for (int i = 0; i <= 20; i++) {
            System.out.print(fib(i) + " ");
        }
        System.out.println();
    }
}
