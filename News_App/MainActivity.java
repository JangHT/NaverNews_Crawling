package com.example.sqllite_test;

import android.app.Activity;
import android.os.Bundle;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteException;
import android.os.Environment;
import android.util.Log;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.Toast;




public class MainActivity  extends Activity {


    private final String dbName = "webnautes";
    private final String tableName = "person";

    private String title[];
    {
        title = new String[]{"Cupcake", "Donut", "Eclair", "Froyo", "Gingerbread", "Honeycomb", "Ice Cream Sandwich", "Jelly Bean", "Kitkat"};
    }

    private final String date[];
    {
        date = new String[]{"Android 1.5", "Android 1.6", "Android 2.0", "Android 2.2", "Android 2.3", "Android  3.0", "Android  4.0", "Android  4.1", "Android  4.4"};
    }

    ArrayList<HashMap<String, String>> personList;

    protected void getData() {


        String path = "C:/Users/HTJang/Desktop/example1/mycsvfile.txt";


        File sdcard = Environment.getExternalStorageDirectory();
        File file = new File(sdcard, path);
        BufferedReader br = null;
        {

            try {
                br = new BufferedReader(new FileReader(file));
            } catch (FileNotFoundException ex) {
                ex.printStackTrace();
            }
            String line = null;

            while (true) {
                try {
                    if (!((line = br.readLine()) != null)) break;
                } catch (IOException e) {
                    e.printStackTrace();
                }
                String[] elements = line.split("\\|\\|");
                List<String> itlist = Arrays.asList(elements);
            }
            try {
                br.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }


/*
    BufferedReader br = null;
    {
        try {
            br = new BufferedReader(new FileReader(path));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        String line = null;
        HashMap<String, String> map = new HashMap<String, String>();

        while (true) {
            try {
                if (!((line = br.readLine()) != null)) break;
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

            System.out.println(line);
            String[] elements = line.split("\\|\\|");
            List<String> itlist = Arrays.asList(elements);
            //ArrayList<String> listOfString = new ArrayList<String>(itlist);
        }
    }
*/


    ListView list;
    private static final String TAG_NAME = "title";
    private static final String TAG_PHONE ="date";

    SQLiteDatabase sampleDB = null;
    ListAdapter adapter;


    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        list = (ListView) findViewById(R.id.listView);
        personList = new ArrayList<HashMap<String,String>>();


        try {


            sampleDB = this.openOrCreateDatabase(dbName, MODE_PRIVATE, null);

            //테이블이 존재하지 않으면 새로 생성합니다.
            sampleDB.execSQL("CREATE TABLE IF NOT EXISTS " + tableName
                    + " (title VARCHAR(20), date VARCHAR(20) );");

            //테이블이 존재하는 경우 기존 데이터를 지우기 위해서 사용합니다.
            sampleDB.execSQL("DELETE FROM " + tableName  );

            //새로운 데이터를 테이블에 집어넣습니다..
            for (int i=0; i<title.length; i++ ) {
                sampleDB.execSQL("INSERT INTO " + tableName
                        + " (title, date)  Values ('" + title[i] + "', '" + date[i]+"');");
            }

            sampleDB.close();

        } catch (SQLiteException se) {
            Toast.makeText(getApplicationContext(),  se.getMessage(), Toast.LENGTH_LONG).show();
            Log.e("", se.getMessage());


        }

        showList();

    }




    protected void showList(){

        try {

            SQLiteDatabase ReadDB = this.openOrCreateDatabase(dbName, MODE_PRIVATE, null);


            //SELECT문을 사용하여 테이블에 있는 데이터를 가져옵니다..
            Cursor c = ReadDB.rawQuery("SELECT * FROM " + tableName, null);

            if (c != null) {


                if (c.moveToFirst()) {
                    do {

                        //테이블에서 두개의 컬럼값을 가져와서
                        String title = c.getString(c.getColumnIndex("title"));
                        String date = c.getString(c.getColumnIndex("date"));

                        //HashMap에 넣습니다.
                        HashMap<String,String> persons = new HashMap<String,String>();

                        persons.put(TAG_NAME,title);
                        persons.put(TAG_PHONE,date);

                        //ArrayList에 추가합니다..
                        personList.add(persons);

                    } while (c.moveToNext());
                }
            }

            ReadDB.close();


            //새로운 adapter를 생성하여 데이터를 넣은 후..
            adapter = new SimpleAdapter(
                    this, personList, R.layout.list_item,
                    new String[]{TAG_NAME,TAG_PHONE},
                    new int[]{ R.id.title, R.id.date}
            );


            //화면에 보여주기 위해 Listview에 연결합니다.
            list.setAdapter(adapter);

            // News 데이터 읽는데 필요한 자료구조
            //HashMap<String, ArrayList<String>> testl;


        } catch (SQLiteException se) {
            Toast.makeText(getApplicationContext(),  se.getMessage(), Toast.LENGTH_LONG).show();
            Log.e("",  se.getMessage());
        }

    }


}
