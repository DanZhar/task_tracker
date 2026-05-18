"""Логика интерактивного меню.

Модуль отвечает за взаимодействие с пользователем через консоль:
главное меню, подменю, ввод данных, вывод отчётов.
"""

from collections import defaultdict

from task_tracker.enums import Priority, Status
from task_tracker.exceptions import (
    DuplicateEntityError,
    EntityNotFoundError,
    InvalidStatusTransitionError,
    StorageError,
    TaskTrackerError,
    ValidationError,
)
from task_tracker.models.project import Project
from task_tracker.models.tasks import Task
from task_tracker.models.user import User
from task_tracker.storage import load_data, save_data


def run_cli(data_file: str = "data.json") -> None:
    try:
        data = load_data(data_file)
    except StorageError as e:
        print(f"Ошибка загрузки данных: {e}")
        answer = _input_lower("Начать с пустого списка проектов? [y/n]: ")
        if answer != "y":
            return
        data = []

    while True:
        try:
            print("\n=== TASK TRACKER ===")
            print("1. Управление проектами")
            print("2. Управление пользователями")
            print("3. Управление задачами")
            print("4. Отчёты")
            print("5. Сохранить и выйти")

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                projects_menu(data)
            elif choice == "2":
                users_menu(data)
            elif choice == "3":
                tasks_menu(data)
            elif choice == "4":
                reports_menu(data)
            elif choice == "5":
                try:
                    save_data(data, data_file)
                    print("Данные сохранены.")
                except StorageError as e:
                    print(f"Ошибка сохранения: {e}")
                break
            else:
                print("Некорректный ввод.")

        except TaskTrackerError as e:
            print(f"Ошибка: {e}")

        except KeyboardInterrupt:
            print("\nПрерывание пользователем.")
            break

        except EOFError:
            print("\nВвод завершён.")
            break


# ── Константы ─────────────────────────────────────────────────────────

STATUS_MAP: dict[str, Status] = {
    "open": Status.OPEN,
    "in_progress": Status.IN_PROGRESS,
    "in_review": Status.IN_REVIEW,
    "done": Status.DONE,
    "closed": Status.CLOSED,
}

PRIORITY_MAP: dict[str, Priority] = {
    "low": Priority.LOW,
    "medium": Priority.MEDIUM,
    "high": Priority.HIGH,
    "critical": Priority.CRITICAL,
}


# ── Вспомогательные функции ───────────────────────────────────────────


def _select_project(data: list) -> Project | None:
    if not data:
        print("Нет доступных проектов.")
        return None

    print("\nПроекты:")
    for i, project in enumerate(data, 1):
        print(f"  {i}: {project.short_display()}")

    idx = input("Выберите проект (номер): ").strip()
    if not idx.isdigit() or not (1 <= int(idx) <= len(data)):
        print("Некорректный номер проекта.")
        return None

    return data[int(idx) - 1]


def _find_task(project: Project, task_id: str) -> Task:
    matches = [t for t in project.tasks if t.id.startswith(task_id)]
    if not matches:
        raise EntityNotFoundError(f"Задача с ID '{task_id}' не найдена.")
    if len(matches) > 1:
        raise EntityNotFoundError(f"Неоднозначный ID '{task_id}': найдено {len(matches)} задач.")
    return matches[0]


def _parse_index(prompt: str, max_value: int) -> int | None:
    """Запросить номер элемента из списка; вернуть индекс или None."""

    raw = input(prompt).strip()
    if not raw.isdigit() or not (1 <= int(raw) <= max_value):
        print("Некорректный номер.")
        return None
    return int(raw) - 1


def _get_project_with_tasks(data: list[Project]) -> tuple[Project, list[Task]] | tuple[None, None]:
    """Выбрать проект и вернуть (project, tasks) или (None, None)."""

    project = _select_project(data)
    if project is None:
        return None, None
    if not project.tasks:
        print("Задач нет.")
        return None, None
    return project, project.tasks


def _input_lower(prompt: str) -> str:
    return input(prompt).strip().lower()


# ── Задачи ────────────────────────────────────────────────────────────


def tasks_menu(data: list[Project]) -> None:
    while True:
        print("\n=== Задачи ===")
        print("1. Создать задачу")
        print("2. Список задач (с фильтрами)")
        print("3. Изменить статус задачи")
        print("4. Назначить исполнителя")
        print("5. Показать детали задачи")
        print("6. Управление подзадачами Epic")
        print("7. Удалить задачу")
        print("8. Назад")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            create_task(data)
        elif choice == "2":
            list_tasks(data)
        elif choice == "3":
            change_task_status(data)
        elif choice == "4":
            assign_task(data)
        elif choice == "5":
            show_task_details(data)
        elif choice == "6":
            manage_epic_subtasks(data)
        elif choice == "7":
            delete_task(data)
        elif choice == "8":
            break
        else:
            print("Некорректный ввод.")


def create_task(data: list[Project]) -> None:
    from task_tracker.models.tasks import Bug, Epic, Feature

    project = _select_project(data)
    if project is None:
        return

    task_type = _input_lower("Тип задачи [bug/feature/epic]: ")
    if task_type not in ("bug", "feature", "epic"):
        print("Неизвестный тип задачи.")
        return

    title = input("Название: ").strip()
    description = input("Описание (Enter для пропуска): ").strip()

    priority_raw = _input_lower("Приоритет [low/medium/high/critical] (Enter = medium): ")
    priority = PRIORITY_MAP.get(priority_raw, Priority.MEDIUM)

    try:
        if task_type == "bug":
            severity_raw = input("Критичность [1-10] (Enter = 1): ").strip()
            severity = int(severity_raw) if severity_raw.isdigit() else 1
            steps = input("Шаги воспроизведения (Enter для пропуска): ").strip()
            task = Bug(
                title=title,
                description=description,
                priority=priority,
                severity=severity,
                steps_to_reproduce=steps,
            )
        elif task_type == "feature":
            bv_raw = input("Бизнес-ценность [1-10] (Enter = 5): ").strip()
            cx_raw = input("Сложность [1-10] (Enter = 5): ").strip()
            task = Feature(
                title=title,
                description=description,
                priority=priority,
                business_value=int(bv_raw) if bv_raw.isdigit() else 5,
                complexity=int(cx_raw) if cx_raw.isdigit() else 5,
            )
        else:
            task = Epic(title=title, description=description, priority=priority)

        project.tasks.append(task)
        print(f"Задача создана: {task.short_display()}")

    except ValidationError as e:
        print(f"Ошибка валидации: {e}")


def list_tasks(data: list[Project]) -> None:
    project, tasks = _get_project_with_tasks(data)
    if project is None:
        return

    print("\nФильтры (оставьте пустым для пропуска):")
    status_raw = _input_lower("  Статус [open/in_progress/in_review/done/closed]: ")
    priority_raw = _input_lower("  Приоритет [low/medium/high/critical]: ")
    type_raw = _input_lower("  Тип [bug/feature/epic]: ")
    assignee_raw = _input_lower("  Исполнитель (имя): ")
    sort_raw = _input_lower("  Сортировка [priority/created_at/estimate]: ")

    if status_raw in STATUS_MAP:
        tasks = [t for t in tasks if t.status == STATUS_MAP[status_raw]]
    elif status_raw:
        print(f"Неизвестный статус '{status_raw}', фильтр пропущен.")

    if priority_raw in PRIORITY_MAP:
        tasks = [t for t in tasks if t.priority == PRIORITY_MAP[priority_raw]]
    elif priority_raw:
        print(f"Неизвестный приоритет '{priority_raw}', фильтр пропущен.")

    if type_raw in ("bug", "feature", "epic"):
        tasks = [t for t in tasks if type(t).__name__.lower() == type_raw]
    elif type_raw:
        print(f"Неизвестный тип '{type_raw}', фильтр пропущен.")

    if assignee_raw:
        tasks = [
            t
            for t in tasks
            if isinstance(t.assignee, User) and assignee_raw in t.assignee.name.lower()
        ]

    if sort_raw == "priority":
        tasks.sort(reverse=True)
    elif sort_raw == "created_at":
        tasks.sort(key=lambda t: t.created_at)
    elif sort_raw == "estimate":
        tasks.sort(key=lambda t: t.estimate(), reverse=True)

    if not tasks:
        print("Нет задач, соответствующих фильтрам.")
        return

    print(f"\nНайдено задач: {len(tasks)}")
    for task in tasks:
        print(f"  [{task.id[:8]}] {task.short_display()}")


def change_task_status(data: list[Project]) -> None:
    from task_tracker.enums import VALID_TRANSITIONS

    project = _select_project(data)
    if project is None:
        return

    task_id = input("ID задачи (можно первые символы): ").strip()
    try:
        task = _find_task(project, task_id)
    except EntityNotFoundError as e:
        print(e)
        return

    available = VALID_TRANSITIONS[task.status]
    if not available:
        print(f"Статус '{task.status.name}' — терминальный, изменение невозможно.")
        return

    print(f"Текущий статус: {task.status.name}")
    print(f"Доступные переходы: {', '.join(s.value for s in available)}")

    new_raw = _input_lower("Новый статус: ")

    if new_raw not in STATUS_MAP:
        print("Неизвестный статус.")
        return

    try:
        task.change_status(STATUS_MAP[new_raw])
        print(f"Статус изменён: {task.status.name}")
    except InvalidStatusTransitionError as e:
        print(f"Недопустимый переход: {e}")


def assign_task(data: list[Project]) -> None:
    project = _select_project(data)
    if project is None:
        return

    if not project.members:
        print("В проекте нет участников.")
        return

    task_id = input("ID задачи (можно первые символы): ").strip()
    try:
        task = _find_task(project, task_id)
    except EntityNotFoundError as e:
        print(e)
        return

    print(f"Текущий исполнитель: {task.assignee.name if isinstance(task.assignee, User) else '–'}")
    print("\nУчастники:")
    for i, member in enumerate(project.members, 1):
        print(f"  {i}. {member.name} ({member.role.value})")
    print("  0. Снять исполнителя")

    raw = input("Выберите участника (номер): ").strip()
    if not raw.isdigit():
        print("Некорректный ввод.")
        return

    idx = int(raw)
    if idx == 0:
        task.assignee = None
        print("Исполнитель снят.")
    elif 1 <= idx <= len(project.members):
        task.assignee = project.members[idx - 1]
        print(f"Исполнитель назначен: {task.assignee.name}")
    else:
        print("Некорректный номер.")


def show_task_details(data: list[Project]) -> None:
    project = _select_project(data)
    if project is None:
        return

    task_id = input("ID задачи (можно первые символы): ").strip()
    try:
        task = _find_task(project, task_id)
    except EntityNotFoundError as e:
        print(e)
        return

    print(task.full_display())


def manage_epic_subtasks(data: list[Project]) -> None:
    from task_tracker.models.tasks import Epic

    project = _select_project(data)
    if project is None:
        return

    epics = [t for t in project.tasks if isinstance(t, Epic)]
    if not epics:
        print("В проекте нет Epic задач.")
        return

    print("\nEpic задачи:")
    for i, epic in enumerate(epics, 1):
        print(f"  {i}. #{epic.id[:8]} {epic.title} ({len(epic.subtasks)} подзадач)")

    epic_idx = _parse_index("Выберите задачу Epic: ", len(epics))
    if epic_idx is None:
        return
    epic = epics[epic_idx]

    while True:
        print(f"\n=== Подзадачи эпика: {epic.title} ===")
        print(f"Оценка: {epic.estimate():.1f}h")
        if epic.subtasks:
            for i, sub in enumerate(epic.subtasks, 1):
                print(f"  {i}. [{sub.id[:8]}] {sub.short_display()}")
        else:
            print("  Подзадач нет.")

        print("\n1. Добавить существующую задачу")
        print("2. Удалить подзадачу")
        print("3. Назад")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            available = [
                t for t in project.tasks if not isinstance(t, Epic) and t not in epic.subtasks
            ]
            if not available:
                print("Нет доступных задач для добавления.")
                continue

            print("\nДоступные задачи:")
            for i, task in enumerate(available, 1):
                print(f"  {i}. [{task.id[:8]}] {task.short_display()}")

            task_idx = _parse_index("Выберите задачу: ", len(available))
            if task_idx is None:
                continue

            try:
                subtask = available[task_idx]
                epic.subtasks.append(subtask)
                project.tasks.remove(subtask)
                print(f"Добавлено: {subtask.title} → оценка эпика: {epic.estimate():.1f}h")
            except ValidationError as e:
                print(f"Ошибка: {e}")

        elif choice == "2":
            if not epic.subtasks:
                print("Подзадач нет.")
                continue

            subtask_idx = _parse_index("Номер подзадачи для удаления: ", len(epic.subtasks))
            if subtask_idx is None:
                continue

            removed = epic.subtasks.pop(subtask_idx)
            project.tasks.append(removed)
            print(f"Удалено: {removed.title}")

        elif choice == "3":
            break
        else:
            print("Некорректный ввод.")


def delete_task(data: list[Project]) -> None:
    project = _select_project(data)
    if project is None:
        return

    task_id = input("ID задачи (можно первые символы): ").strip()
    try:
        task = _find_task(project, task_id)
    except EntityNotFoundError as e:
        print(e)
        return

    confirm = _input_lower(f"Удалить '{task.title}'? [y/n]: ")
    if confirm == "y":
        project.tasks.remove(task)
        print("Задача удалена.")
    else:
        print("Отменено.")


# ── Проекты ───────────────────────────────────────────────────────────


def projects_menu(data: list[Project]) -> None:
    while True:
        print("\n=== Проекты ===")
        print("1. Список проектов")
        print("2. Создать проект")
        print("3. Удалить проект")
        print("4. Показать детали проекта")
        print("5. Назад")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            list_projects(data)
        elif choice == "2":
            create_project(data)
        elif choice == "3":
            delete_project(data)
        elif choice == "4":
            show_project_details(data)
        elif choice == "5":
            break
        else:
            print("Некорректный ввод.")


def list_projects(data: list[Project]) -> None:
    if not data:
        print("Проектов нет.")
        return

    print("\n=== Список проектов ===")
    for i, project in enumerate(data, 1):
        print(f"  {i}. {project.short_display()}")


def create_project(data: list[Project]) -> None:
    name = input("Название проекта: ").strip()
    if not name:
        print("Название не может быть пустым.")
        return

    if any(p.name.lower() == name.lower() for p in data):
        print(f"Проект '{name}' уже существует.")
        return

    try:
        project = Project(name=name)
        data.append(project)
        print(f"Проект создан: {project.name}")
    except ValidationError as e:
        print(f"Ошибка валидации: {e}")
    except DuplicateEntityError as e:
        print(f"Дубликат: {e}")


def delete_project(data: list[Project]) -> None:
    if not data:
        print("Проектов нет.")
        return

    project = _select_project(data)
    if project is None:
        return

    warnings = []
    if project.tasks:
        warnings.append(f"задач: {len(project.tasks)}")
    if project.members:
        warnings.append(f"участников: {len(project.members)}")
    if warnings:
        print(f"Внимание! В проекте есть {', '.join(warnings)}.")

    confirm = _input_lower(f"Удалить проект '{project.name}'? [y/n]: ")
    if confirm == "y":
        data.remove(project)
        print(f"Проект '{project.name}' удалён.")
    else:
        print("Отменено.")


def show_project_details(data: list[Project]) -> None:
    project = _select_project(data)
    if project is None:
        return
    print(project.full_display())


# ── Пользователи ──────────────────────────────────────────────────────


def users_menu(data: list[Project]) -> None:
    while True:
        print("\n=== Пользователи ===")
        print("1. Список участников проекта")
        print("2. Добавить участника в проект")
        print("3. Удалить участника из проекта")
        print("4. Назад")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            list_members(data)
        elif choice == "2":
            add_member(data)
        elif choice == "3":
            remove_member(data)
        elif choice == "4":
            break
        else:
            print("Некорректный ввод.")


def list_members(data: list[Project]) -> None:
    project = _select_project(data)
    if project is None:
        return

    if not project.members:
        print("В проекте нет участников.")
        return

    print(f"\n=== Участники: {project.name} ===")
    for i, member in enumerate(project.members, 1):
        task_count = sum(1 for t in project.tasks if t.assignee == member)
        print(f"  {i}. [{member.id[:8]}] {member.name} ({member.role.value}) — задач: {task_count}")


def add_member(data: list[Project]) -> None:
    from task_tracker.enums import Role

    project = _select_project(data)
    if project is None:
        return

    name = input("Имя участника: ").strip()
    if not name:
        print("Имя не может быть пустым.")
        return

    if any(m.name.lower() == name.lower() for m in project.members):
        print(f"Участник с именем '{name}' уже есть в проекте.")
        return

    role_map = {
        "developer": Role.DEVELOPER,
        "qa": Role.QA,
        "team_lead": Role.TEAM_LEAD,
        "pm": Role.PM,
    }
    role_raw = _input_lower(f"Роль [{'/'.join(role_map)}]: ")
    role = role_map.get(role_raw, Role.DEVELOPER)

    try:
        user = User(name=name, role=role)
        project.members.append(user)
        print(f"Участник добавлен: {user.name} ({user.role.value})")
    except ValidationError as e:
        print(f"Ошибка валидации: {e}")
    except DuplicateEntityError as e:
        print(f"Дубликат: {e}")


def remove_member(data: list[Project]) -> None:
    project = _select_project(data)
    if project is None:
        return

    if not project.members:
        print("В проекте нет участников.")
        return

    print(f"\nУчастники {project.name}:")
    for i, member in enumerate(project.members, 1):
        print(f"  {i}. {member.name} ({member.role.value})")

    idx = _parse_index("Выберите участника для удаления (номер): ", len(project.members))
    if idx is None:
        return

    member = project.members[idx]
    assigned_tasks = [t for t in project.tasks if t.assignee == member]

    if assigned_tasks:
        print(f"У участника {len(assigned_tasks)} назначенных задач:")
        for task in assigned_tasks:
            print(f"  — {task.short_display()}")
        confirm = _input_lower("Снять назначение и удалить участника? [y/n]: ")
        if confirm != "y":
            print("Отменено.")
            return
        for task in assigned_tasks:
            task.assignee = None

    project.members.remove(member)
    print(f"Участник '{member.name}' удалён.")


# ── Отчёты ────────────────────────────────────────────────────────────


def reports_menu(data: list[Project]) -> None:
    while True:
        print("\n=== Отчёты ===")
        print("1. Сводка по проекту")
        print("2. Задачи по исполнителям")
        print("3. Оценка трудоёмкости")
        print("4. Назад")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            report_project_summary(data)
        elif choice == "2":
            report_tasks_by_assignee(data)
        elif choice == "3":
            report_estimate(data)
        elif choice == "4":
            break
        else:
            print("Некорректный ввод.")


def report_project_summary(data: list[Project]) -> None:
    from collections import Counter

    project, tasks = _get_project_with_tasks(data)
    if project is None:
        return

    status_cnt = Counter(task.status for task in tasks)
    type_cnt = Counter(type(task).__name__ for task in tasks)
    priority_cnt = Counter(task.priority for task in tasks)

    print(f"\n=== Сводка: {project.name} ===")
    print(f"Всего задач: {len(tasks)}")

    print("По статусам:")
    for status in Status:
        cnt = status_cnt.get(status, 0)
        if cnt:
            print(f"  {status.name} – {cnt}")

    print("По типам:")
    for task_type in ("Bug", "Feature", "Epic"):
        cnt = type_cnt.get(task_type, 0)
        if cnt:
            print(f"  {task_type} – {cnt}")

    print("По приоритетам:")
    for priority in sorted(Priority, key=lambda x: x.value, reverse=True):
        cnt = priority_cnt.get(priority, 0)
        if cnt:
            print(f"  {priority.name} – {cnt}")


def report_tasks_by_assignee(data: list[Project]) -> None:
    project, tasks = _get_project_with_tasks(data)
    if project is None:
        return

    assigned: dict = defaultdict(list)
    unassigned = []

    for task in tasks:
        if isinstance(task.assignee, User):
            assigned[task.assignee].append(task)
        else:
            unassigned.append(task)

    print("\n=== Задачи по исполнителям ===")
    for user, user_tasks in assigned.items():
        print(f"{user.short_display()}:")
        for i, task in enumerate(user_tasks, 1):
            print(f"  {i}. {task.short_display()}")

    if unassigned:
        print("Не назначены:")
        for i, task in enumerate(unassigned, 1):
            print(f"  {i}. {task.short_display()}")


def report_estimate(data: list[Project]) -> None:
    project, tasks = _get_project_with_tasks(data)
    if project is None:
        return

    total_estimate = sum(task.estimate() for task in tasks)
    total_by_types: dict = {}
    for task in tasks:
        type_name = type(task).__name__
        total_by_types[type_name] = total_by_types.get(type_name, 0.0) + task.estimate()

    top5 = sorted(tasks, key=lambda x: x.estimate(), reverse=True)[:5]

    print("=== Оценка трудоёмкости ===")
    print(f"Общая оценка: {total_estimate:.1f} ч")

    print("По типам:")
    for type_name in ("Bug", "Feature", "Epic"):
        hours = total_by_types.get(type_name, 0.0)
        if hours:
            print(f"  {type_name} – {hours:.1f} ч")

    print("Топ-5 самых трудоёмких:")
    for i, task in enumerate(top5, 1):
        print(f"  {i}. {task.label()} {task.title} – {task.estimate():.1f} ч")
