CREATE TABLE IF NOT EXISTS strategic_goals (
  id INT AUTO_INCREMENT PRIMARY KEY,
  dimension VARCHAR(64) NOT NULL,
  objetivo VARCHAR(512) NOT NULL,
  plan_id INT NOT NULL,
  meta_estrategica VARCHAR(512) NOT NULL,
  estrategia_periodo VARCHAR(512) NOT NULL,
  descripcion_indicador VARCHAR(1024) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_strategic_goals_plan
    FOREIGN KEY (plan_id) REFERENCES strategic_plans(id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  INDEX idx_dimension (dimension),
  INDEX idx_objetivo (objetivo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

