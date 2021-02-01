package com.github.surfaces.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Точка многоугольника
 */
@AllArgsConstructor
@Data
@NoArgsConstructor
public class Point {
    private int x;
    private int y;
    private int z;
}
