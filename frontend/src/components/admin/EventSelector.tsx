import React, { useState, useEffect, useRef } from 'react';
import { ChevronDown, Plus, X, Calendar, Loader } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { getWorkshops, createWorkshop, Workshop } from '../../services/api';

interface EventSelectorProps {
  selectedEvent: string; // workshop title (= event name)
  onEventSelect: (eventName: string) => void;
  onEventIdChange?: (eventId: string) => void; // also emit the workshop ID
  token: string | null;
}

const EventSelector: React.FC<EventSelectorProps> = ({ selectedEvent, onEventSelect, onEventIdChange, token }) => {
  const [events, setEvents] = useState<Workshop[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [newEventName, setNewEventName] = useState('');
  const [isLoadingEvents, setIsLoadingEvents] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Load events on mount
  useEffect(() => {
    const loadEvents = async () => {
      setIsLoadingEvents(true);
      try {
        const workshops = await getWorkshops();
        setEvents(workshops);
      } catch (error) {
        console.error('Failed to load events:', error);
      } finally {
        setIsLoadingEvents(false);
      }
    };
    loadEvents();
  }, []);

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
        setIsCreating(false);
        setNewEventName('');
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Focus input when creating
  useEffect(() => {
    if (isCreating && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isCreating]);

  const handleCreateEvent = async () => {
    if (!newEventName.trim() || !token) return;

    setIsSaving(true);
    try {
      const newWorkshop = await createWorkshop(token, {
        title: newEventName.trim(),
        date: new Date().toISOString().split('T')[0],
        instructor: 'ACM',
        level: 'Beginner' as const,
      });
      setEvents(prev => [...prev, newWorkshop]);
      onEventSelect(newWorkshop.title);
      onEventIdChange?.(newWorkshop.id);
      setNewEventName('');
      setIsCreating(false);
      setIsOpen(false);
    } catch (error) {
      console.error('Failed to create event:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleCreateEvent();
    }
    if (e.key === 'Escape') {
      setIsCreating(false);
      setNewEventName('');
    }
  };

  return (
    <div className="space-y-2">
      <label className="text-sm font-bold text-slate-700 dark:text-slate-200 uppercase tracking-wider flex items-center gap-2">
        <Calendar size={14} />
        Event / Workshop *
      </label>

      <div ref={dropdownRef} className="relative">
        {/* Trigger button */}
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          className={`w-full flex items-center justify-between px-4 py-3 border-2 rounded-lg font-mono transition-all outline-none ${isOpen
            ? 'border-primary ring-4 ring-primary/20 bg-slate-800 text-white'
            : selectedEvent
              ? 'border-slate-700 bg-slate-800 text-white'
              : 'border-slate-700 bg-slate-800 text-slate-500'
            }`}
        >
          <span className={selectedEvent ? 'text-white' : 'text-slate-500'}>
            {isLoadingEvents ? 'Loading events...' : selectedEvent || 'Select an event...'}
          </span>
          {isLoadingEvents ? (
            <Loader size={16} className="animate-spin text-slate-400" />
          ) : (
            <ChevronDown
              size={16}
              className={`text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}
            />
          )}
        </button>

        {/* Dropdown */}
        <AnimatePresence>
          {isOpen && !isLoadingEvents && (
            <motion.div
              initial={{ opacity: 0, y: -4 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -4 }}
              transition={{ duration: 0.15 }}
              className="absolute z-50 w-full mt-1 rounded-lg border border-slate-700 bg-slate-800 shadow-2xl overflow-hidden"
            >
              {/* Events list */}
              <div className="max-h-48 overflow-y-auto">
                {events.length === 0 && !isCreating && (
                  <div className="px-4 py-3 text-xs text-slate-500 font-mono text-center">
                    No events yet. Create one below.
                  </div>
                )}
                {events.map((event) => (
                  <button
                    type="button"
                    key={event.id}
                    onClick={() => {
                      onEventSelect(event.title);
                      onEventIdChange?.(event.id);
                      setIsOpen(false);
                    }}
                    className={`w-full text-left px-4 py-2.5 text-sm transition-colors flex items-center gap-2 ${selectedEvent === event.title
                      ? 'bg-primary/15 text-primary font-bold'
                      : 'text-slate-300 hover:bg-slate-700/50'
                      }`}
                  >
                    <div className={`w-2 h-2 rounded-full flex-shrink-0 ${selectedEvent === event.title ? 'bg-primary' : 'bg-slate-600'
                      }`} />
                    <span className="truncate">{event.title}</span>
                  </button>
                ))}
              </div>

              {/* Divider */}
              <div className="border-t border-slate-700" />

              {/* Create new event */}
              {isCreating ? (
                <div className="p-2 flex gap-2">
                  <input
                    ref={inputRef}
                    type="text"
                    value={newEventName}
                    onChange={(e) => setNewEventName(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Event name..."
                    className="flex-1 px-3 py-2 text-sm rounded-md bg-slate-900 border border-slate-600 text-white font-mono placeholder:text-slate-600 outline-none focus:border-primary"
                  />
                  <button
                    type="button"
                    onClick={handleCreateEvent}
                    disabled={!newEventName.trim() || isSaving}
                    className="px-3 py-2 rounded-md bg-primary text-white text-xs font-bold disabled:opacity-40 hover:bg-primary/80 transition-colors"
                  >
                    {isSaving ? <Loader size={12} className="animate-spin" /> : 'Add'}
                  </button>
                  <button
                    type="button"
                    onClick={() => { setIsCreating(false); setNewEventName(''); }}
                    className="px-2 py-2 rounded-md text-slate-400 hover:text-red-400 transition-colors"
                  >
                    <X size={14} />
                  </button>
                </div>
              ) : (
                <button
                  type="button"
                  onClick={() => setIsCreating(true)}
                  className="w-full flex items-center gap-2 px-4 py-2.5 text-sm text-emerald-400 hover:bg-slate-700/50 transition-colors font-bold"
                >
                  <Plus size={14} />
                  Create New Event
                </button>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default EventSelector;
