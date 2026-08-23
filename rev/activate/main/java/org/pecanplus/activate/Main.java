package org.pecanplus.activate;

public class Main {

    public static String BROAD_REGEX = "^pecan\\{\\d{4}-20\\d{2}-\\d{4}-\\d{2}26}$";

    public static void main(String[] args) {
        System.out.println("-".repeat(75));
        System.out.println("Proprietary Software 9000");
        System.out.println();
        System.out.println("This software is protected by Placebo Obfuscation technology.");
        System.out.println("-".repeat(75));

        if (args.length == 0) {
            System.out.println("Unlicensed software, please specify a license key.");
            System.out.println("Debug flag for developers: --debug");
            System.out.println("Goodbye!");
            System.exit(1);
        }

        if (args.length > 1) {
            System.out.println("Error: Too many arguments provided.");
            System.exit(1);
        }

        String inp = args[0];

        if (inp.equalsIgnoreCase("--debug")) {
            System.out.println("Starting debug mode...");
            System.out.println();
            System.out.println("--- Activation System Debug ---");
            System.out.println("Reverse engineering is usually required to resolve activation issues.");
            System.out.println();
            System.out.println("Debugging complete. Bye!");
            System.exit(1);
        }

        if (inp.length() != 26 || !inp.matches(BROAD_REGEX)) {
            System.out.println("Error: Invalid license key.");
            System.exit(1);
        }

        final char[] pat = {'5', '3', '0', '8', '0', '0', '5', '1', '8', '6', '6', '9'};
        final int[] pos = {22, 21, 19, 18, 17, 16, 14, 13, 9, 8, 7, 6};

        for (int i = 0; i < pos.length; i++) {
            if (inp.charAt(pos[i]) != pat[i]) {
                System.out.println("Error: Invalid license key.");
                System.exit(1);
            }
        }

        System.out.println();
        System.out.println("--- Software Activated ---");
        System.out.println("License Key: " + inp);
        System.out.println("This program has been activated successfully. Thank you for your purchase.");
        System.out.println();
    }

}