package com.example;

/**
 * Main class for the Java project
 */
public class Main {
    
    /**
     * Main method - entry point of the application
     * @param args command line arguments
     */
    public static void main(String[] args) {
        System.out.println("Hello, World!");
        System.out.println("Welcome to your new Java project!");
        
        // Example of using command line arguments
        if (args.length > 0) {
            System.out.println("Command line arguments:");
            for (int i = 0; i < args.length; i++) {
                System.out.println("  " + (i + 1) + ": " + args[i]);
            }
        }
    }
}

