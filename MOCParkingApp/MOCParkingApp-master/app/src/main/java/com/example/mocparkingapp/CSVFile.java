package com.example.mocparkingapp;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

/*
 * Credit to https://javapapers.com/android/android-read-csv-file/ for the tutorial
 */

class CSVFile {
    private InputStream inputStream;

    // The inputStream component represents the raw data in a specified file outside this class
    CSVFile(InputStream inputStream){
        this.inputStream = inputStream;
    }

    // .read() parses the raw data through a BufferedReader that returns a List of String[].
    List<String[]> read(){
        List<String[]> resultList = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
        try {
            String csvLine;
            while ((csvLine = reader.readLine()) != null) {
                resultList.add(csvLine.split(","));
            }
        }

        // Beginning of Exception Handling
        catch (IOException ex) {
            throw new RuntimeException("Error in reading CSV file: "+ex);
        }
        finally {
            try {
                inputStream.close();
            }
            catch (IOException e) {
                throw new RuntimeException("Error while closing input stream: "+e);
            }
        }
        return resultList;
        // End of Exception Handling

    }
}