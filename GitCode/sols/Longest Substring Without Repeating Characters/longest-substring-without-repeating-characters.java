class Solution {
    public static int lengthOfLongestSubstring(String s) {
        if(s.length()==0) return 0;
        int max = 0;
        int left = 0;
        int right = 0;
        Set<Character> ch = new HashSet<>();
        while(right<s.length()){
            if(ch.contains(s.charAt(right))){
                ch.remove(s.charAt(left));
                left++;
            }
            else{
                ch.add(s.charAt(right));
                right++;
            }
            max = Math.max(max, right-left+1);
        }
        return max-1;
    }
}