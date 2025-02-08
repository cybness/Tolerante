import java.util.Scanner;

class Main {
    public static void main(String[] args) {
        Scanner entero = new Scanner(System.in);
        System.out.println('\n'+ "Introdue un número entero");
        String numero = entero.nextLine();
        try{
            int resultado = Integer.parseInt(numero);
            System.out.println("Felicidades, introduciste el número " + resultado);

        } catch (NumberFormatException e) {
            System.out.println("Nope.");
        } finally {
            entero.close();
        }
            
    }
}
