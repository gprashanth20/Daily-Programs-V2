public class MergeSort {
    static void sort(int[] arr, int lo, int hi) {
        if (lo >= hi) return;
        int mid = lo + (hi - lo) / 2;
        sort(arr, lo, mid);
        sort(arr, mid + 1, hi);
        merge(arr, lo, mid, hi);
    }

    static void merge(int[] arr, int lo, int mid, int hi) {
        int[] left = java.util.Arrays.copyOfRange(arr, lo, mid + 1);
        int[] right = java.util.Arrays.copyOfRange(arr, mid + 1, hi + 1);
        int i = 0, j = 0, k = lo;
        while (i < left.length && j < right.length) {
            arr[k++] = left[i] <= right[j] ? left[i++] : right[j++];
        }
        while (i < left.length) arr[k++] = left[i++];
        while (j < right.length) arr[k++] = right[j++];
    }

    public static void main(String[] args) {
        int[] data = {38, 27, 43, 3, 9, 82, 10};
        sort(data, 0, data.length - 1);
        System.out.println(java.util.Arrays.toString(data));
    }
}
