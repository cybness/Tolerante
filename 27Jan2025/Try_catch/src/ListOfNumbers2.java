import java.io.*;
import java.util.Vector;

public class ListOfNumbers2 {
    private Vector<Integer> victor;
    private static final int SIZE = 10;

    public ListOfNumbers2() {
        victor = new Vector<Integer>(SIZE);
        for (int i = 0; i < SIZE; i++) {
            victor.addElement(i);  // Usando autoboxing, no es necesario new Integer(i)
        }

        this.readList("Trycatch/infile.txt");
        this.writeList();
    }

    public void readList(String fileName) {
        String line = null;
        try (RandomAccessFile raf = new RandomAccessFile(fileName, "r")) {
            if (raf.length() == 0) {  // Verificar si el archivo está vacío
                System.err.println("Error: El archivo " + fileName + " está vacío.");
                return;  // Salir del método sin procesar nada
            }
    
            while ((line = raf.readLine()) != null) {
                try {
                    Integer i = Integer.parseInt(line);  // Convertir a Integer
                    victor.addElement(i);  // Agregar al Vector
                } catch (NumberFormatException e) {
                    System.err.println("Error: Línea inválida en el archivo: " + line);
                }
            }
        } catch (FileNotFoundException fnf) {
            System.err.println("Error: Archivo " + fileName + " no encontrado.");
        } catch (IOException io) {
            System.err.println("Error de entrada/salida: " + io.toString());
        }
    }
    

    public void writeList() {
        PrintWriter out = null;

        try {
            out = new PrintWriter(new FileWriter("Trycatch/outfile.txt"));
        
            for (int i = 0; i < victor.size(); i++) {
                out.println("Value at: " + i + " = " + victor.elementAt(i));
            }
        } catch (IOException e) {
            System.err.println("Caught IOException: " + e.getMessage());
        } finally {
            if (out != null) {
                System.out.println("Closing PrintWriter");
                out.close();
            } else {
                System.out.println("PrintWriter not open");
            }
        }
    }

    public static void main(String[] args) {
        new ListOfNumbers2();
    }
}
