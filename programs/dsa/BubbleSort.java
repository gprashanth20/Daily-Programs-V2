public class BubbleSort {
    static void sort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int tmp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = tmp;
                    swapped = true;
                }
            }
            if (!swapped) break; // already sorted
        }
    }

    public static void main(String[] args) {
        int[] data = {5, 1, 4, 2, 8, 0, 9, 3};
        sort(data);
        System.out.println(java.util.Arrays.toString(data));
    }
}
