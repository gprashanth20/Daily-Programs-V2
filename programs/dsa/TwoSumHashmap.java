import java.util.HashMap;
import java.util.Map;

public class TwoSumHashmap {
    static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (seen.containsKey(complement)) {
                return new int[] { seen.get(complement), i };
            }
            seen.put(nums[i], i);
        }
        throw new IllegalArgumentException("No two sum solution");
    }

    public static void main(String[] args) {
        int[] nums = {2, 7, 11, 15};
        int[] idx = twoSum(nums, 9);
        System.out.println("Indices: " + idx[0] + ", " + idx[1]);
    }
}
