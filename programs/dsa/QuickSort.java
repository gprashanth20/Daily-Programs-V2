public class QuickSort {
    static void sort(int[] arr, int lo, int hi) {
        if (lo >= hi) return;
        int p = partition(arr, lo, hi);
        sort(arr, lo, p - 1);
        sort(arr, p + 1, hi);
    }

    static int partition(int[] arr, int lo, int hi) {
        int pivot = arr[hi];
        int i = lo - 1;
        for (int j = lo; j < hi; j++) {
            if (arr[j] < pivot) {
                i++;
                int tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
            }
        }
        int tmp = arr[i + 1]; arr[i + 1] = arr[hi]; arr[hi] = tmp;
        return i + 1;
    }

    public static void main(String[] args) {
        int[] data = {10, 7, 8, 9, 1, 5};
        sort(data, 0, data.length - 1);
        System.out.println(java.util.Arrays.toString(data));
    }
}
