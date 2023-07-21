class Solution {
    // public static String longestPalindrome(String s) {
    //     StringBuilder sb1 = new StringBuilder();
    //     for (int i = 0; i <= s.length(); i++) {
    //         for (int j = i; j <= s.length(); j++) {
    //             String temp = s.substring(i, j);
    //             if(ispali(temp) && temp.length()>sb1.length()){
    //                 sb1.delete(0, sb1.length());
    //                 sb1.append(temp);
    //             }
    //         }
    //     }
    //     return sb1.toString();
    // }
    // public static boolean ispali(String s){
    //     int left = 0, right = s.length()-1;
    //     while(left<right){
    //         if(s.charAt(left) != s.charAt(right)){
    //             return false;
    //         }
    //         left++;
    //         right--;
    //     }
    //     return true;
    // }
    public static String longestPalindrome(String s){
        if(s.length()<1) return "";
        int start = 0, end=0;
        for (int i = 0; i < s.length(); i++) {
            int len = Math.max(maxpali(s, i, i), maxpali(s, i, i+1));
            if(len > end-start){
                start = i - ((len-1)/2);
                end = i + (len/2);
            }
        }
        return s.substring(start, end+1);
    }
    public static int maxpali(String s, int left, int right){
        if(left>right || s == null) return 0;
        while(left>=0 && right<s.length() && s.charAt(left) == s.charAt(right)){
            left--;
            right++;
        }
        return right - left - 1;
    }
}