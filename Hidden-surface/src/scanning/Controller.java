package scanning;

import javafx.fxml.FXML;
import javafx.scene.canvas.Canvas;

import java.io.IOException;
import java.util.ArrayList;

public class Controller {

    //  Полотно, где будут отображены многоугольники
    @FXML
    private Canvas canvas = new Canvas();

    /*
     *  Инициализация сцены
     *  @throws IOException: исключение ввода/вывода
     */
    public void initialize() throws IOException {
        ArrayList <Polygon> polygons = Main.readingData();
        Main.lineScanning(polygons, canvas);
    }

}
