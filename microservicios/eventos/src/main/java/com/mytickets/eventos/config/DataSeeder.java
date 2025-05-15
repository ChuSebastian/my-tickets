package com.mytickets.eventos.config;

import com.mytickets.eventos.model.Categoria;
import com.mytickets.eventos.model.Evento;
import com.mytickets.eventos.repository.CategoriaRepository;
import com.mytickets.eventos.repository.EventoRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.*;

@Component
public class DataSeeder implements CommandLineRunner {

    private final CategoriaRepository categoriaRepository;
    private final EventoRepository eventoRepository;

    public DataSeeder(CategoriaRepository categoriaRepository, EventoRepository eventoRepository) {
        this.categoriaRepository = categoriaRepository;
        this.eventoRepository = eventoRepository;
    }

    @Override
    public void run(String... args) {
        if (categoriaRepository.count() == 0) {
            List<String> nombres = List.of(
                    "Concierto", "Teatro", "Feria", "Festival", "Cine",
                    "Danza", "Exposición", "Deporte", "Charla", "Taller"
            );

            for (String nombre : nombres) {
                Categoria categoria = new Categoria();
                categoria.setNombre(nombre);
                categoriaRepository.save(categoria);
            }
        }

        if (eventoRepository.count() == 0) {
            List<Categoria> categorias = categoriaRepository.findAll();
            Random random = new Random();

            List<Evento> eventos = new ArrayList<>();

            for (int i = 1; i <= 20000; i++) {
                Evento evento = new Evento();
                evento.setNombre("Evento " + i);
                evento.setDescripcion("Descripción del evento número " + i);
                evento.setFecha(LocalDate.now().plusDays(random.nextInt(365)).toString());
                evento.setLugar("Lugar " + (random.nextInt(100) + 1));
                evento.setPrecio(10 + random.nextInt(91)); // entre 10 y 100
                evento.setImagen("/img" + (random.nextInt(10) + 1) + ".jpg");
                evento.setCategoria(categorias.get(random.nextInt(categorias.size())));
                eventos.add(evento);

                // Guardar en lotes de 500
                if (eventos.size() == 500) {
                    eventoRepository.saveAll(eventos);
                    eventos.clear();
                }
            }

            // Guardar los últimos eventos
            if (!eventos.isEmpty()) {
                eventoRepository.saveAll(eventos);
            }

            System.out.println("✅ Base de datos poblada con 10 categorías y 20,000 eventos.");
        }
    }
}
