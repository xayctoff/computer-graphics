package com.github.surfaces.model;

import javafx.scene.paint.Color;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * Многоугольник
 */
@AllArgsConstructor
@Data
@NoArgsConstructor
public class Polygon {

    /**
     * Коэффициент A уравнения плоскости
     */
    private double a;

    /**
     * Коэффициент B уравнения плоскости
     */
    private double b;

    /**
     * Коэффициент C уравнения плоскости
     */
    private double c;

    /**
     * Коэффициент D уравнения плоскости
     */
    private double d;

    /**
     * Номер многоугольника
     */
    private int number;

    /**
     * Цвет
     */
    private Color color;

    /**
     * Левое активное ребро
     */
    private Edge left;

    /**
     * Правое активное ребро
     */
    private Edge right;

    /**
     * Список рёбер
     */
    private List<Edge> edges;

    /**
     * Список точек
     */
    private List<Point> points;
}
