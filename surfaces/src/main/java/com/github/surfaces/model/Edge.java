package com.github.surfaces.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Ребро многоугольника
 */
@AllArgsConstructor
@Data
@NoArgsConstructor
public class Edge {
    private Point start;
    private Point finish;
}
