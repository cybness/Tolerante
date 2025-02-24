import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;
import org.json.JSONObject;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

class InternetMonitor extends Thread {
    public InternetMonitor() {
        setDaemon(true);
    }

    @Override
    public void run() {
        while (true) {
            try {
                Thread.sleep(2000);
                if (checkInternet()) {
                    System.out.println("\n [\u2713] Conexion a LastFM estable.");
                } else {
                    System.out.println("\n [\u2717] Conexion a LastFM perdida.");
                }
            } catch (InterruptedException e) {
                System.out.println("El hilo de monitoreo de Internet ha sido interrumpido.");
            }
        }
    }

    private boolean checkInternet() {
        try {
            URL url = new URL("https://www.last.fm/");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("HEAD");
            connection.setConnectTimeout(2000);
            connection.setReadTimeout(2000);
            int responseCode = connection.getResponseCode();
            return (200 <= responseCode && responseCode <= 399);
        } catch (IOException e) {
            return false;
        }
    }
}

public class LastFm {
    private static final String API_KEY = "XXXXXXXXX";
    
    public static void main(String[] args) {
        InternetMonitor monitor = new InternetMonitor();
        monitor.start();

        Scanner scanner = new Scanner(System.in);
        System.out.print("Ingrese el nombre del album: ");
        String albumName = scanner.nextLine().trim().toLowerCase();;
        System.out.print("Ingrese el nombre del artista: ");
        String artistName = scanner.nextLine().trim().toLowerCase();
        scanner.close();

        try {
            String encodedArtist = URLEncoder.encode(artistName, StandardCharsets.UTF_8.toString());
            String encodedAlbum = URLEncoder.encode(albumName, StandardCharsets.UTF_8.toString());
            String url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=" + API_KEY + "&artist=" + encodedArtist + "&album=" + encodedAlbum + "&format=json";

            System.out.println("Buscando informacion del album: " + albumName + ". . . ");
            HttpURLConnection connection = (HttpURLConnection) new URL(url).openConnection();
            connection.setRequestMethod("GET");
            connection.setConnectTimeout(5000);
            connection.setReadTimeout(5000);
            
            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }
            reader.close();
            
            JSONObject jsonResponse = new JSONObject(response.toString());
            if (jsonResponse.has("album")) {
                JSONObject album = jsonResponse.getJSONObject("album");
                String title = album.getString("name");
                String listeners = album.getString("listeners");
                System.out.println("Titulo: " + title);
                System.out.println("Oyentes: " + listeners);
               
                // Obtener el tracklist
                if (album.has("tracks")) {
                    System.out.println("\nTracklist:");
                    JSONObject tracks = album.getJSONObject("tracks");
                    for (int i = 0; i < tracks.getJSONArray("track").length(); i++) {
                        String track = tracks.getJSONArray("track").getJSONObject(i).getString("name");
                        System.out.println((i + 1) + ".- " + track);
                    }
                } else {
                    System.out.println("No se encontro el tracklist.");
                }
            } else {
                System.out.println("No se encontro informacion del album.");
            }
        } catch (IOException e) {
            System.out.println("Error al conectar con la API de Last.fm");
        }
    }
}
