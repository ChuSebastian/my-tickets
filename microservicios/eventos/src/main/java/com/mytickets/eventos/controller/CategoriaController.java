package com.mytickets.eventos.controller;

import com.mytickets.eventos.dto.CategoriaDTO;
import com.mytickets.eventos.model.Categoria;
import com.mytickets.eventos.repository.CategoriaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/categorias")
public class CategoriaController {

    @Autowired
    private CategoriaRepository categoriaRepository;

    @GetMapping
    public List<CategoriaDTO> getCategorias() {
        return categoriaRepository.findAll().stream()
                .map(cat -> new CategoriaDTO(cat.getId(), cat.getNombre()))
                .collect(Collectors.toList());
    }

    @PostMapping
    public CategoriaDTO crearCategoria(@RequestBody CategoriaDTO dto) {
        Categoria categoria = new Categoria();
        categoria.setNombre(dto.getNombre());
        Categoria guardada = categoriaRepository.save(categoria);
        return new CategoriaDTO(guardada.getId(), guardada.getNombre());
    }
}
