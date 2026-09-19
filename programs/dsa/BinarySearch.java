public class BinarySearch {
    // Iterative binary search - O(log n)
    static int search(int[] arr, int target) {
        int lo = 0, hi = arr.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }

    // Recursive version
    static int searchRecursive(int[] arr, int lo, int hi, int target) {
        if (lo > hi) return -1;
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] == target) return mid;
        return arr[mid] < target
            ? searchRecursive(arr, mid + 1, hi, target)
            : searchRecursive(arr, lo, mid - 1, target);
    }

    public static void main(String[] args) {
        int[] data = {2, 5, 8, 12, 16, 23, 38, 45, 56, 72};
        System.out.println("Iterative: index of 23 -> " + search(data, 23));
        System.out.println("Recursive: index of 45 -> " + searchRecursive(data, 0, data.length - 1, 45));
        System.out.println("Missing value -> " + search(data, 99));
    }
}
